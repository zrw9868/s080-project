import imageio

pickups = []
dropoffs = []

for time in ["morning","afternoon","evening","night"]:
	pu = "gif/"+time + "-pu.png"
	do = "gif/"+time + "-do.png"
	pickups.append(imageio.imread(pu))
	dropoffs.append(imageio.imread(do))

imageio.mimsave('gif/pickups_map.gif', pickups,duration=1)
imageio.mimsave('gif/dropoffs_map.gif', dropoffs,duration=1)