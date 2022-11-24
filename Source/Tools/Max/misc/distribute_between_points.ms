/*
:type tool
:group Uncategorised
:category Utilities|Placement
:supported_hosts [max]
*/

(
	try(destroyDialog roDistribute)catch()
	global roDistribute
	
	global instances = #()
	
	function lerp x y a=
	(
		return y * a + x * (1.0 - a)
	)
	
	rollout roDistribute "Distribute Stairs Parts" width:225
	(
		label lbl_start "Start:" across:4
		spinner spn_startX width:50 align:#left range:(point3 -9999.0 9999.0 0.0)
		spinner spn_startY width:50 align:#left range:(point3 -9999.0 9999.0 0.0)
		spinner spn_startZ width:50 align:#left range:(point3 -9999.0 9999.0 0.0)
		
		label lbl_end "End:" across:4
		spinner spn_endX width:50 align:#left range:(point3 -9999.0 9999.0 100.0)
		spinner spn_endY width:50 align:#left range:(point3 -9999.0 9999.0 100.0)
		spinner spn_endZ width:50 align:#left range:(point3 -9999.0 9999.0 100.0)
		
		label lbl_spacing "Spacing:" across:4 align:#left
		spinner spn_spacing width:50 align:#left range:(point3 -9999.0 9999.0 25.0)
		label lbl_null ""
		label lbl_null2 ""
		
		button btn_distribute "Distribute" width:200
		button btn_delete "Clear" width:200
		
		groupbox spc_01 "" height:1 align:#center
		
		label lbl_description "Currently does a [pos / 2.54] to assume \nwe are using cm. This may need fixing." height:30 --align:#left
		
		on btn_distribute pressed do
		(
			local parent = selection[1]
			
			local vec_start = point3 spn_startX.value spn_startY.value spn_startZ.value
			local vec_end = point3 spn_endX.value spn_endY.value spn_endZ.value
			
			if(selection[1] != undefined) do
			(
				local dist_x = abs (spn_startX.value - spn_endX.value)
				local dist_y = abs (spn_startY.value - spn_endY.value)
				local dist_r = sqrt ( (dist_x * dist_x) + (dist_y * dist_y) )
				
				dist_r = if dist_r == 0 then 1.0 else dist_r
				spn_spacing.value = if spn_spacing.value == 0 then 1.0 else spn_spacing.value
				
				local num_loops = (integer (dist_r + 0.01)) / (integer (spn_spacing.value + 0.01))
				
				for i = 0 to num_loops do
				(
					local fraction =  (float i) / (float num_loops)
					
					local instance_location = (lerp vec_start vec_end fraction) / 2.54
						
						
					local instance_reference = instance selection[1]
					instance_reference.position = instance_location
					
					append instances instance_reference
				)
				
				
				
			)
			
		)
		
		on btn_delete pressed do
		(
			for i in instances do
			(
				delete i
			)
			instances = #()
		)

	)
	
	createDialog roDistribute
)