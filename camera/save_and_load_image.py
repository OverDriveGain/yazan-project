from PIL import Image
import stapipy as st
from utils import CAM_OUTPUT_DIR

# Number of images to grab #ToDo Comment need fixing
number_of_images_to_grab = 1


def take_photo(st, st_device, output_dir=CAM_OUTPUT_DIR, file_suffix=''):
    # ToDo find a way to not close camera fater each photo
    # ToDo some lines shouldn't be used inside a loop in the future
    try:
        # Display DisplayName of the device.
        print('Device=', st_device.info.display_name)
        # File for image file
        filename_prefix = st_device.info.display_name + file_suffix
        file_prefix = output_dir + '/' + filename_prefix
        file_location = output_dir + '/' + filename_prefix + ".StApiRaw"  # os.path.join(tempfile.gettempdir(),
        #  filename_prefix + ".StApiRaw")

        # Create a datastream object for handling image stream data.
        st_datastream = st_device.create_datastream()

        # Start the image acquisition of the host (local machine) side.
        st_datastream.start_acquisition(number_of_images_to_grab)

        # Start the image acquisition of the camera side.
        st_device.acquisition_start()

        is_image_saved = False
        while st_datastream.is_grabbing:
            with st_datastream.retrieve_buffer() as st_buffer:
                # Check if the acquired data contains image data.
                if st_buffer.info.is_image_present:
                    # Create an image object.
                    st_image = st_buffer.get_image()
                    # Display the information of the acquired image data.
                    print("BlockID={0} Size={1} x {2} First Byte={3}".format(
                        st_buffer.info.frame_id,
                        st_image.width, st_image.height,
                        st_image.get_image_data()[0]))

                    # Create a still image file handling class object (filer)
                    st_stillimage_filer = st.create_filer(st.EStFilerType.StillImage)

                    # Save the image file as StApiRaw file format.
                    print("Saving {0} ... ".format(file_location), end="")
                    st_stillimage_filer.save(st_image,
                                             st.EStStillImageFileFormat.StApiRaw, file_location)
                    print("done.")
                    is_image_saved = True
                else:
                    # If the acquired data contains no image data.
                    print("Image data does not exist.")

        # Load StapiRaw and process the image.
        if is_image_saved:
            # Load image
            st_stillimage_filer = st.create_filer(st.EStFilerType.StillImage)
            print("Loading {0} ... ".format(file_location), end="")
            st_image = st_stillimage_filer.load(file_location)
            print("done.")

            # Convert image to BGR8 format.
            st_converter = st.create_converter(st.EStConverterType.PixelFormat)
            st_converter.destination_pixel_format = \
                st.EStPixelFormatNamingConvention.BGR8
            st_image = st_converter.convert(st_image)

            # Save as bitmap, tiff, png, jpg, csv
            save_list = {st.EStStillImageFileFormat.PNG: '.png',
                         }
            for file_format, file_ext in save_list.items():
                file_location = output_dir + '/' + filename_prefix + file_ext
                print("Saving {0} ... ".format(file_location), end="")
                st_stillimage_filer.save(st_image, file_format, file_location)
                print("done.")
        print("Resizing")
        png_path = file_prefix + '.png'
        im = Image.open(png_path)
        print(im.size)

        new_size = im.resize((705, 380))
        new_size.save(png_path)
        # Stop the image acquisition of the camera side
        st_device.acquisition_stop()

        # Stop the image acquisition of the host side
        st_datastream.stop_acquisition()
        return png_path
    except Exception as exception:
        print(exception)


def take_photos_helper(count=8):
    # Initialize StApi before using.
    st.initialize()
    # Create a system object for device scan and connection.
    st_system = st.create_system()
    # Connect to first detected device.
    st_device = st_system.create_first_device()
    output_images = []
    for i in range(0, count):
        output_images.append(take_photo(st, st_device, file_suffix=str(i)))
    return output_images
