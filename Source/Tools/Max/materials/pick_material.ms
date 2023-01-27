/*
:type tool
:category Utilities|Materials
:group Materials
:supported_hosts [max]
:summary Picks the material on a selected poly in the material editor
:note Only supports editable poly
*/
(
	tool PickMaterial
	(		
		on mousePoint val do
		(
			mxscene = python.import "pymxs.juniper.scene"
			
			node_ = mxscene.pick_node viewpoint get_inode:True
			if(node_ != undefined) do
			(
				node_real = maxOps.getNodeByHandle node_.Handle
				node_class = classOf node_real
				if(node_class == editable_poly or node_class == polyMeshObject) do
				(
					face = mxscene.hit_test_face node_ viewpoint

					--select node_real
					--max modify mode
					--subObjectLevel = 4
					--polyOp.setFaceSelection node_real face

					matEditor.open()
					mat_index = 0
					for i = 1 to mEditMaterials.count while mat_index == 0 do
					(
						if(node_real.material == getMeditMaterial i) do
						(
							mat_index = i
						)
					)

					mEdit.setActiveMtlSlot mat_index True
					-- TODO~ Tools Library: Need a way to switch to the current multi material index
				)
			)
			#stop
		)
	)

	startTool PickMaterial
)