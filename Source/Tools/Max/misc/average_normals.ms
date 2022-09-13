/*
:type tool
:group Uncategorised
:supported_hosts [max]
:category Uncategorised
*/
(
	clearListener()
	object_center = selection[1].center
	
	convertToMesh selection[1]
	
	
	max_ = getVert selection[1] 1
	min_ = getVert selection[1] 1
	for i = 1 to getNumVerts(selection[1]) do
	(
		vpos = getVert selection[1] i
		if(vpos.x > max_.x) do (max_.x = vpos.x)
		if(vpos.y > max_.y) do (max_.y = vpos.y)
		if(vpos.z > max_.z) do (max_.z = vpos.z)
		if(vpos.x < min_.x) do (min_.x = vpos.x)
		if(vpos.y <min_.y) do (min_.y = vpos.y)
		if(vpos.z < min_.z) do (min_.z = vpos.z)
	)
	c = (max_ + min_) / 2
	
	
	for i = 1 to getNumVerts(selection[1]) do
	(
		dir_to_center =  normalize ((getVert selection[1] i) - c)
		setNormal selection[1] i dir_to_center
	)
	
	
	positions = #()
	face_indices = #()
	todel = #{}
	for i = 1 to getNumFaces selection[1] do
	(
		fc = meshOp.getFaceCenter selection[1] i
		ind = findItem positions fc
		if(ind == 0) then
		(
			todel[i] = false
			append positions fc
			append face_indices #(i)
		)
		else
		(
			todel[i] = true
			--append todel i
			append face_indices[ind] i
		)
	)
	
	meshOp.deleteFaces (selection[1]) todel
)