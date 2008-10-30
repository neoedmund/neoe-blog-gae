iconNames = file("icon.list").readlines()
def getName(key):
	return "icon%s.png" % iconNames[key % len(iconNames)]