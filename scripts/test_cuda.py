import tensorflow as tf
from tensorflow.python.platform import build_info as build
from tensorflow.python.client import device_lib

def check_cuda():
    print("TensorFlow version:", tf.__version__)

    # List all available devices
    print("Available devices:")
    devices = device_lib.list_local_devices()
    for device in devices:
        print(device)

    # Check if TensorFlow is using a GPU
    list_physical_devices = tf.config.list_physical_devices('GPU')
    if list_physical_devices:
        print("GPU is available")
    else:
        print("GPU is not available")

    print()
    print('-' * 50)
    print('-' * 50)
    print(f"tensorflow version: {tf.__version__}")
    print(f"Cuda Version: {build.build_info['cuda_version']}")
    print(f"Cudnn version: {build.build_info['cudnn_version']}")
    print(f"< {list_physical_devices} >")
    print('-' * 50)
    print('Check if GPU is available:')
    print()


if __name__ == "__main__":
    check_cuda()