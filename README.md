# pygenshin-core
This is outdated. If you can figure out what this does, and what you need to update, your are welcome to use this for anything you want.


Hint: everything under /pygenshin/data/ needs to be updated. 
See what resolution tiles are, download the new map image and crop it so it is evenly divided into tiles.
I wrote a script for that from scratch by looking at the folder/file structure, so you will probably figure it out.
Update map_data.json by fetching it from the same site you downloaded a map from. It needs some simple restructuring, so you'll need to do that.

Then you need to recalculate and save kpts.npy and desc.npy, which stand for keypoints and descriptors. Read about opencv visual recognition,
SIFT, nad how to save desciptors and keypoints to disk. I would've helped you with that part,
 but I'm writing this from a phone and I dont think I'll have access to my PC soon.
 
 Good luck, stranger.
