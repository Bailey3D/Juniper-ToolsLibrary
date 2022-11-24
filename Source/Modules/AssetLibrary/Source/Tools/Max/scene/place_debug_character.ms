/*
:type tool
:category Asset Library|Debug
:group Debug
:supported_hosts [max]
:summary Places a default debug character (from the asset in the asset library)
*/

with undo off
(

	node_name = "__ASSETLIBRARYDEBUGCHAR__"
	char_node = undefined
	
	function create_char_node = 
	(
		current_nodes = for i in objects collect i
		
		if((getNodeByName node_name) == undefined) do
		(
			-- get asset path
			alp = python.import "tools_library.asset_library.paths"
			asset_library_root = alp.root()
			char_path = asset_library_root + "\\content\\Common\\Geometry\\Standard\\Shapes\\meshes\\SM_Geo_Shape_Char.FBX"
			-- import fbx and search for new node
			importFile char_path #noPrompt using:FBXIMP
		)
		
		for i in objects where ((findItem current_nodes i) == 0) do
		(
			char_node = i
		)
		
        char_node.scale = [1, 1, 1]
        char_node.name = node_name
		return char_node
	)
		
	tool create_debug_char
	(
		on mousePoint click do
		(
			tx = undefined
			
			if(click == 1) then
			(
				if(char_node != undefined) do
				(
					char_node.position = gridPoint	
				)
			)
			else
			(
				return #stop
			)
		)

		on mouseMove click do
		(
			if(char_node != undefined) do
			(
				char_node.position = gridPoint
			)
		)
	)

	create_char_node()
	startTool create_debug_char
)