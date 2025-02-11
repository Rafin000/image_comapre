import tensorflow as tf

# Check if GPU is available and configure memory growth
def setup_gpu():
    physical_devices = tf.config.list_physical_devices('GPU')
    if physical_devices:
        print("GPU is available.")
        for device in physical_devices:
            tf.config.experimental.set_memory_growth(device, True)
    else:
        print("GPU is not available, using CPU.")

setup_gpu()
