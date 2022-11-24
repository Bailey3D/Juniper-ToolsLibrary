/*
:type tool
:group Uncategorised
:category Utilities|Modelling
:supported_hosts [max]
*/

(
	local export_path = "X:/Assets/geometry/blockout/"
	
	--// Rollout
	global roMain
	try(destroydialog roMain)catch()
	
	--// Create a STD_Ground type using input width and height
	--// subdivs will truncate relative to the aspect ratio of the plane
	function CreateGround width:250 length:250 subdivs:4 =
	(
		target_name = ("SM_STD_Ground_" + width as string + "x" + length as string)
		
		delete (for i in objects where (i.name == target_name) collect i)
		
		aspect_ratio = if (width > length) then #(1, (floor (width / length)) as integer) else #((floor (length / width)) as integer, 1)
		
		target = plane()
		target.length = length
		target.width = width
		target.lengthsegs = subdivs / aspect_ratio[2]
		target.widthsegs = subdivs / aspect_ratio[1]
		
		target.position = point3 (width / 2.0) (length / 2.0)  0
		target.pivot = point3 0 0 0
		rotate target (eulerangles 0 0 180)
		target.name = target_name
	)
	
	function CreateWall width:250 height:250 depth:5 subdivs:4 =
	(
		target_name = ("SM_STD_Wall_" + width as string + "x" + height as string)
		
		delete (for i in objects where (i.name == target_name) collect i)
		
		aspect_ratio = if (width > height) then #(1, (floor (width / height)) as integer) else #((floor (height / width)) as integer, 1)
		
		target = plane()
		target.length = height
		target.width = width
		target.lengthsegs = subdivs / aspect_ratio[2]
		target.widthsegs = subdivs / aspect_ratio[1]
		
		target.position = point3 (width / 2.0) (height / 2.0)  depth
		target.pivot = point3 0 0 0
		rotate target (eulerangles 90 0 -90)
		target.name = target_name
	)

	function CreateDoor width:100 height:200 depth:5 subdivs:1 type:#regular =
	(
		target_name = ("SM_STD_Door_" + type)
		
		target = Box()
		target.length = depth
		target.width = width
		target.height = height
		
		delete (for i in objects where (i.name == target_name) collect i)
		
		target.position = point3 (width / 2) 0 0
		
		target.name = target_name
		target.pivot = point3 0 0 0
		rotate target (eulerangles 0 0 -90)
	)
	
	rollout roMain "Blockout Generator"
	(
		/*group "Walls"
		(
			spinner spn_wallwidth "Width"
			spinner spn_wallheight "Height"
			spinner spn_wallthickness "Thickness"
		)
		
		group "Ground"
		(
			spinner spn_width "Scale"
		)
		
		group "Doors"
		(
			spinner spn_doorwidth "Width"
			spinner spn_doorheight "Height"
		)
		
		group "Windows"
		(
			spinner spn_windowsngwidth "Single: Width"
			spinner spn_windowsngheight "Height"
			
			spinner spn_windowdblwidth "Double: Width"
			spinner spn_windowdblheight "Height"
		)*/
		
		button btn_gen "Generate" width:150
		button btn_export "Export" width:150
		
		on btn_gen pressed do
		(
			CreateGround length:250 width:250 subdivs:8
			CreateGround length:125 width:250 subdivs:8
			CreateGround length:125 width:125 subdivs:4

			CreateWall width:250 height:250 depth:5 subdivs:8
			CreateWall width:250 height:125 depth:5 subdivs:8
			CreateWall width:125 height:250 depth:5 subdivs:8
			CreateWall width:125 height:125 depth:5 subdivs:4
			
			CreateDoor width:100 height:200 depth:5
		)
		
		on btn_export pressed do
		(
			for geo in objects where ((findstring geo.name "SM_STD") != undefined) do
			(
				select geo
				exportFile (export_path + geo.name) #noprompt selectedOnly:true using:FBXEXP
			)
		)
		
	)
	
	createdialog roMain	
	
	clearlistener()
	
)