/*
:type startup
:callbacks [startup]
:desc Custom material plugin used to pick .material files for use in Max
*/
plugin material AssetLibraryMaterial
name:"Asset Library Material"
classID:#(692425,477581)
extends:Standard replaceUI:true version:1
(
  parameters main rollout:params
  (
	filepath type:#string default:""
  )
  
  rollout params "Properties"
  (
	button btnPickMaterial "Pick Material.." width:200
	 
	  
	  function update_material_path path_ =
	  (
		if(path_ == "") then
		(
			filepath = ""
			btnPickMaterial.text = "Pick Material.."
		)
		else
		(
			filepath = path_
			btnPickMaterial.text = "Current Material: " + getFileNameFile path_
		)
	  )
	  
	  
	  on btnPickMaterial pressed do
	  (
		file_utils = python.import "juniper.utilities.filemgr"
		al = python.import "asset_library"		 
		  
		if(filepath != "") then
		(
			start_path = al.paths.unmap_path filepath
		)
		else
		(
			start_path = al.paths.root() + "\\content"  
		)
		
		mat_path = 	file_utils.pick_file title:"Pick Shader" start:start_path file_types:"Material (*.material)"
		  
		if(mat_path != "") do
		(
			filepath = al.paths.map_path(mat_path)
			update_material_path mat_path
		)
	  )
	  
	  
	  on params open do
	  (
		  update_material_path filepath
	  )
	  
  )
  
  
  on create do
  (
	params.update_material_path filepath
  )
  
)