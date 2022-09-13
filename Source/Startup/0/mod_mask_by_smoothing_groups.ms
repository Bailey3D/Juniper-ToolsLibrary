/*
:type startup
:callbacks [startup]
:desc Modifier for use on Editable Poly objects which deletes all faces not matching the target smoothing group
*/
plugin simpleMeshMod MaskBySmoothingGroups
name:"Mask By Smoothing Group"
classID:#(694675,477222)
replaceUI:true
version:1
(
	parameters main rollout:params
	(
		smoothing_id ui:spn_smoothing_id default:1 type:#integer animatable:false
	) 

	rollout params "Parameters"
	(
		spinner spn_smoothing_id "Smoothing Group:" range:[1, 32, 1] type:#integer width:100 align:#right
	) 

	on modifyMesh do
	(
		clearListener()
		
		delete_faces = #()
		
		for i = 1 to (meshOp.getNumFaces mesh) do
		(
			smooth_group = getFaceSmoothGroup mesh i
			if(not (bit.get smooth_group smoothing_id)) do
			(
				append delete_faces i
			)
		)
		
		meshOp.deleteFaces mesh delete_faces
		update mesh
	)
)