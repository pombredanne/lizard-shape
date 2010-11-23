# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.db import models
from django.utils import simplejson as json

from treebeard.al_tree import AL_Node
from nens.sobek import HISFile

from lizard_map.models import Legend
from lizard_map.models import LegendPoint

# The default location from MEDIA_ROOT to upload files to.
UPLOAD_TO = "lizard_shape/shapes"
UPLOAD_HIS = "lizard_shape/his"


class ShapeNameError(Exception):
    pass


class Shape(models.Model):
    """
    Here you can upload your shapefiles: .dbf, .prj, .shp, .shx
    files. Select a shape template and you got your shapefile layout.
    """

    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)

    shp_file = models.FileField(upload_to=UPLOAD_TO)
    dbf_file = models.FileField(upload_to=UPLOAD_TO)
    shx_file = models.FileField(upload_to=UPLOAD_TO)
    prj_file = models.FileField(upload_to=UPLOAD_TO)

    his = models.ForeignKey('His', null=True, blank=True)
    his_parameter = models.CharField(
        max_length=80, null=True, blank=True,
        help_text=u'i.e. Discharge max (m\\xb3/s) for Discharge max (m\xb3/s)')

    template = models.ForeignKey('ShapeTemplate')

    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        """Check if constraints are met before saving model."""
        shp_first = self.shp_file.name.rpartition('.')
        dbf_first = self.dbf_file.name.rpartition('.')
        shx_first = self.shx_file.name.rpartition('.')
        prj_first = self.prj_file.name.rpartition('.')

        if shp_first[-1] != 'shp':
            raise ShapeNameError(
                "Uploaded shp_file doest not have extension .shp.")
        if dbf_first[-1] != 'dbf':
            raise ShapeNameError(
                "Uploaded dbf_file doest not have extension .dbf.")
        if shx_first[-1] != 'shx':
            raise ShapeNameError(
                "Uploaded shx_file doest not have extension .shx.")
        if prj_first[-1] != 'prj':
            raise ShapeNameError(
                "Uploaded prj_file doest not have extension .prj.")

        if shp_first[0] == dbf_first[0] == shx_first[0] == prj_first[0]:
            super(Shape, self).save(*args, **kwargs)
        else:
            raise ShapeNameError(
                "Uploaded files do not have common filename base.")

    def get_adapter_layer_json_list(self):
        """
        Calculates all adapter_layer_jsons from available legends and
        return in list.
        """
        result = []
        # Add all shapelegends.
        result.extend([s.adapter_layer_json
                       for s in self.shapelegend_set.all()])
        # Add all shapelegendspoints.
        result.extend([s.adapter_layer_json
                       for s in self.shapelegendpoint_set.all()])
        return result

    def timeseries(self, location_name, start=None, end=None):
        """
        Returns timeseries from hisfile in a dict associating
        timestamp to value. Returns [] if no hisfile defined.
        """
        if self.his and self.his_parameter:
            hf = self.his.hisfile()
            return hf.get_timeseries(
                location_name, self.his_parameter, start=start, end=end)
        return []


class ShapeTemplate(models.Model):
    """
    A shape template contains fieldnames. It also has configured
    legends and fields referenced to it. Create a template once and
    use it many times in shapes.
    """

    name = models.CharField(
        max_length=80,
        help_text='Display name.')
    id_field = models.CharField(
        max_length=20, null=True, blank=True,
        help_text='The id field must be filled for searching and his files.')
    name_field = models.CharField(
        max_length=20, null=True, blank=True,
        help_text='The name field must be filled for mouseovers, popups.')

    def __unicode__(self):
        return '%s' % self.name


class ShapeField(models.Model):
    """
    Which fields do we want to display in a popup? Used by adapter in
    lizard-map.
    """
    name = models.CharField(max_length=80)
    field = models.CharField(max_length=20)

    shape_template = models.ForeignKey('ShapeTemplate')

    def __unicode__(self):
        return u'%s - %s' % (self.shape, self.name)


class Category(AL_Node):
    """
    Tree structure for ordering objects.

    Optionally connect shapes to nodes.
    """

    name = models.CharField(
        max_length=80,
        help_text='i.e. max debiet.')
    slug = models.SlugField(
        max_length=20, unique=True)
    parent = models.ForeignKey(
        'Category', null=True, blank=True)

    # For treebeard.
    node_order_by = ['name']

    shapes = models.ManyToManyField('Shape', null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.name


class ShapeLegend(Legend):
    """
    Legend for shapefile:
    - Which field to use for value?
    """

    shape_template = models.ForeignKey('ShapeTemplate')
    value_field = models.CharField(max_length=20)

    def __unicode__(self):
        return '%s - %s' % (self.shape_template, self.descriptor)

    def adapter_layer_json(self, shape):
        """
        Defines adapter_layer_json for adapter_shapefile (from
        lizard-map).
        """
        id_field = (self.shape_template.id_field
                    if self.shape_template.id_field else "")
        name_field = (self.shape_template.name_field
                      if self.shape_template.name_field else "")
        display_fields = [{'name': sf.name, 'field': sf.field}
                          for sf in self.shape_template.shapefield_set.all()]
        result = ((
                '{"layer_name": "%s", '
                '"legend_id": "%d", '
                '"legend_type": "ShapeLegend", '
                '"value_field": "%s", '
                '"value_name": "%s", '
                '"layer_filename": "%s", '
                '"search_property_id": "%s", '
                '"search_property_name": "%s", '
                '"shape_id": "%d", '
                '"display_fields": %s}') % (
                str(self),
                self.id,
                self.value_field,
                self.descriptor,
                shape.shp_file.path,
                id_field,
                name_field,
                shape.id,
                json.dumps(display_fields)))
        return result


class ShapeLegendPoint(LegendPoint):
    """
    Legend for point shapefile.
    """

    shape_template = models.ForeignKey(
        'ShapeTemplate',
        help_text='Select a shape template for visualization.')
    value_field = models.CharField(max_length=20)

    def __unicode__(self):
        return '%s - %s' % (self.shape_template, self.descriptor)

    def adapter_layer_json(self, shape):
        """
        Defines adapter_layer_json for adapter_shapefile (from
        lizard-map).
        """
        id_field = (self.shape_template.id_field
                    if self.shape_template.id_field else "")
        name_field = (self.shape_template.name_field
                      if self.shape_template.name_field else "")
        display_fields = [{'name': sf.name, 'field': sf.field}
                          for sf in self.shape_template.shapefield_set.all()]
        result = ((
                '{"layer_name": "%s", '
                '"legend_id": "%d", '
                '"legend_type": "ShapeLegendPoint", '
                '"value_field": "%s", '
                '"value_name": "%s", '
                '"layer_filename": "%s", '
                '"search_property_id": "%s", '
                '"search_property_name": "%s", '
                '"shape_id": "%d", '
                '"display_fields": %s}') % (
                str(self),
                self.id,
                self.value_field,
                self.descriptor,
                shape.shp_file.path,
                id_field,
                name_field,
                shape.id,
                json.dumps(display_fields)))
        return result


class His(models.Model):
    """
    Sobek HIS files and their relation to a shapefile.
    """

    name = models.CharField(max_length=80,
                            help_text='Display name.')
    filename = models.FileField(upload_to=UPLOAD_HIS)

    def __unicode__(self):
        return '%s' % self.name

    def hisfile(self):
        result = HISFile(self.filename.path)
        return result
