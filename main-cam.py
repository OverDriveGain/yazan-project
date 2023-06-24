#from camera.save_and_load_image import take_photos_helper
from classifier.predict import predict_image_list
from GUI.start import start_grid_vis
from utils import write_predict_result, read_predict_result
# Take photo from camera

#output_images = take_photos_helper(8)
output_images = ["storage/cam_photos/STC-MBS500U3V(22K5341)0.png",
                 "storage/cam_photos/STC-MBS500U3V(22K5341)1.png",
                 "storage/cam_photos/STC-MBS500U3V(22K5341)2.png",
                 "storage/cam_photos/STC-MBS500U3V(22K5341)3.png",
                 "storage/cam_photos/STC-MBS500U3V(22K5341)4.png",
                 "storage/cam_photos/STC-MBS500U3V(22K5341)5.png",
                 "storage/cam_photos/STC-MBS500U3V(22K5341)6.png",
                 "storage/cam_photos/STC-MBS500U3V(22K5341)7.png",
                 ]
res = predict_image_list(output_images)
write_predict_result(res)
res_storage = read_predict_result()
start_grid_vis(res_storage)
# Predict
# store prediction
# visualize in GUI
