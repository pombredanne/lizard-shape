Changelog of lizard-shape
===================================================


2.6 (unreleased)
----------------

- Nothing changed yet.


2.5 (2012-12-04)
----------------

- Slightly changed popup styling.


2.4 (2012-11-27)
----------------

- Properly set dependency versions.


2.3 (2012-11-22)
----------------

- Fixed bug in __unicode__ of ShapeTemplate. It crashes on some
  characters.

- Support mixed flot/matplotlib (IE8) graphs.

- Add Bootstrap table styling.


2.2 (2012-10-04)
----------------

- Add GDAL dependency which is referenced in a management command.


2.1.1 (2012-06-26)
------------------

- Fix bug in ShapeField's __unicode__ that made it throw an exception in
  case the field has a ShapeTemplate (this is bad).


2.1 (2012-05-29)
----------------

- Fix colorfield references in migrations.

- UI fixes.


2.0 (2012-05-18)
----------------

- Fix colorfield import.

- Added edit link

- Updated layout for bootstrap.

- Changed .txt extensions to .rst.


1.29 (2012-04-26)
-----------------

- Changed description of shape templates.


1.28 (2012-04-06)
-----------------

- Changed signature of two functions in AdapterShapefile
  (collage_detail_data_description and collage_detail_edit_action) to
  comply with lizard-map 3.26.

- Required lizard-map 3.26.

- Added .gitignore

1.27.1 (2012-03-28)
-------------------

- Nothing changed yet.


1.27 (2012-03-28)
-----------------

- Raising a validationerror when a category's parent field points at
  itself. This leads to an infinite recursion error in the __unicode__,
  rendering the admin inaccessible (to fix the error...).

- Increased radius in the adapter's search(), Dave complained it was
  impossibly small.

1.26 (2012-01-23)
-----------------

- Don't show 'Grafiek' on the collage detail page since we don't
  actually have one, and don't show the dialog to edit graph options.


1.25 (2012-01-17)
-----------------

- Removed old breadcrumbs code because it didn't work with the
  new version anymore. Now needs lizard-map 3.18.

- Checking for case-insensitive extension, so .SHP is just fine for .shp.


1.24 (2011-12-21)
-----------------

- Adding to collage from the popup works now (L3). Needs a lizard_map
  upgrade to 3.9


1.23 (2011-11-04)
-----------------

- Fixed a bug that prevented the view class from working.


1.22 (2011-11-04)
-----------------

- Made view class based for lizard-map 3.3

- Changed template to use new workspace / collage tags

- Changed buildout and setup to require lizard-map >= 3.3

1.21.1 (2011-09-22)
-------------------

- Fixed typo in the "clearer error message" from 1.21 that crashed the
  logger.


1.21 (2011-09-22)
-----------------

- Clearer error message when converting coordinates to google doesn't work. To
  aid debugging that particular error.

- Also raising WorkspaceItemError when looking up shapes via a slug, not just
  when looking it up via a primary key.

- Fixed icon color in legend, first prefered is color_inside if
  none then color #2957.

- Added errorcheck for #3033. When the shapefile does not exist, the
  adapter.search function will now return with an empty list.


1.20 (2011-06-30)
-----------------

- Added index field to ShapeLegendSingleClass to control the order of
  the legend rows. #2985


1.19 (2011-06-29)
-----------------

- Adapter.extent now uses ogr.GetExtent function. Faster and easier.


1.18 (2011-06-17)
-----------------

- Limiting number of search results to 3 instead of 10.


1.17 (2011-06-16)
-----------------

- Added prj field to Shape model. The adapter (layers.py) now uses
  Shape.prj instead of reading the file.

Note: After upgrading, run the management command
lizard_shape_update_prj. This re-saves all Shape models in order to
fill the prj fields.


1.16 (2011-06-03)
-----------------

- Enabled transparency slide in lizard-shape.

- Depending on lizard-map >= 1.80 now as that does away with the javascript
  map hover handler. More performance!


1.15 (2011-05-11)
-----------------

- Added dependency in migration on lizard-map so that lizard-map's legend
  exists before our migration requires it.


1.14.2 (2011-05-06)
-------------------

- #2551 Removed header "Veld" and "Waarde" from popup.

- #2663 Fixed untransformed radius.


1.14.1 (2011-05-02)
-------------------

- Added error checking when legend class color is not filled in.


1.14 (2011-04-21)
-----------------

- Removed unnecessary workspace_manager and date_range_form stuff. It
  is also incompatible with map >= 1.71.


1.13 (2011-04-20)
-----------------

- Added dependency on lizard-map >= 1.68 in setup.py (WorkspaceItemError)

- Removed pin on lizard-map 1.36 in buildout.cfg

- Removed pin on lizard-ui 1.24 (version conflict with latest lizard-map)


1.12 (2011-04-14)
-----------------

- Removed header from popup (looks better).


1.11 (2011-03-10)
-----------------

- Changed Category.__unicode__ so that the category pull down menu
  shows the tree location.


1.10 (2011-03-10)
-----------------

- Added shape_slug option to adapter constructor.


1.9 (2011-02-08)
----------------

- Bugfixed breadcrumbs.


1.8 (2011-02-03)
----------------

- Bugfix breadcrumbs.


1.7 (2011-02-01)
----------------

- Added option crumbs_prepend (see lizard_ui).


1.6 (2011-01-27)
----------------

- Removed coords[0] in layers. Previously caused an error with polygons.


1.5 (2011-01-20)
----------------

- Added sorting to models.

- Added unique constraint to shape template name.

- Added fields, filters to admin interface. Improved maintainability
  a little bit, but it still needs improvement.

- Added option to go to pages with user given category root.


1.4.1 (2011-01-13)
------------------

- Added error check on hisfile.


1.4 (2011-01-13)
----------------

- Added icon and color to ShapeLegendClass. The icons will display in
  the workspace.

- Added info button to shape homepage when shape has a description.

- Added datetime of hisfiles to popup.

- Added unit to graphs.

- Added category ancestors to category admin page.

- Added extent function to layer.

- Added search support for shapefiles with WGS84 projection.


1.3 (2011-01-11)
----------------

- Added support for shapefiles with WGS84 projection.

- Bugfix is_exact.

- Added tests.


1.2 (2011-01-04)
----------------

- Improved performance for layer search.

- Added tests.

- Removed unused function get_adapter_layer_json_list.


1.1 (2010-12-16)
----------------

- Added more shapefile options.

- Added initial South migration.


1.0 (2010-12-10)
----------------

- Update categories view.


0.13 (2010-12-10)
-----------------

- Simplify __unicode__ function of ShapeLegendClass. Very important
  for various views (i.e. results in flow).


0.12 (2010-12-09)
-----------------

- Name in hover popup now uses ShapeFields first field instead of the
  value_field.

- Added optional legend class labels.


0.11 (2010-12-08)
-----------------

- Bugfix polygon popup.


0.10 (2010-12-06)
-----------------

- Rename title from Flow to Shape.


0.9 (2010-12-02)
----------------

- Bugfix popup when clicking on single object.

- Updated admin.

- Updates model help_text.


0.8 (2010-12-02)
----------------

- Make use of field_type: image, link or normal.


0.7 (2010-12-02)
----------------

- Added field_type to ShapeField.

- Bugfix ShapeLegendClass.


0.6 (2010-11-29)
----------------

- Added adapter.legend for LEGEND_TYPE_SHAPELEGENDCLASS.

- Added popup_shape template (moved from lizard_map).

- Pinned lizard-map 1.25.

- Improved adapter.


0.5 (2010-11-25)
----------------

- Extend shapefile adapter with adapter functions.

- Implemented shapelegendclass. Refactored legend stuff.

- Moved shapefile adapter from lizard-map to here.


0.4 (2010-11-11)
----------------

- Pinned lizard-map 1.23.


0.3 (2010-11-11)
----------------

- Changed json to django.utils.simplejson as json.


0.2 (2010-11-11)
----------------

- Moved adapter_layer_json functions to model functions.

- Added tests and fixtures.

- Pinned newest lizard-map and lizard-ui.


0.1 (2010-11-01)
----------------

- First working version: lines are showed on map.

- Initial library skeleton created by nensskel.  [Jack]
