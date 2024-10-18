import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf 

class ImageClassifierApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Classifier")

        # Labels for displaying the image and result
        self.image_label = tk.Label(master, text="No image selected.")
        self.image_label.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

        # Buttons for picking image and classifying it
        self.pick_image_button = tk.Button(master, text="Pick Image", command=self.pick_image)
        self.pick_image_button.pack()

        self.classify_button = tk.Button(master, text="Classify Image", command=self.classify_image)
        self.classify_button.pack()

        self.image = None
        self.model = self.load_model("assets/mobilenet_v1_1.0_224.tflite")
        self.labels = self.load_labels("assets/labels.txt")

    def load_model(self, model_path):
        # Load the TFLite model
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter

    def load_labels(self, labels_path):
        # Load labels from the text file
        with open(labels_path, 'r') as f:
            return [line.strip() for line in f.readlines()]

    def pick_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image = Image.open(file_path)
            self.image = self.image.resize((224, 224))  # Resize image to match model input
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.image_tk, text="")  # Update image label

    def classify_image(self):
        if self.image is not None:
            # Preprocess image for classification
            input_data = np.array(self.image) / 255.0
            input_data = np.expand_dims(input_data, axis=0).astype(np.float32)

            # Set input tensor
            input_details = self.model.get_input_details()
            output_details = self.model.get_output_details()

            self.model.set_tensor(input_details[0]['index'], input_data)
            self.model.invoke()

            # Get output tensor
            output_data = self.model.get_tensor(output_details[0]['index'])
            top_k_indices = output_data[0].argsort()[-5:][::-1]  # Get top 5 indices
            results = [(self.labels[i], output_data[0][i]) for i in top_k_indices]

            # Show results
            result_text = "\n".join([f"{label}: {confidence:.2f}" for label, confidence in results])
            self.result_label.config(text=result_text)
        else:
            messagebox.showwarning("Warning", "Please pick an image first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageClassifierApp(root)
    root.mainloop()
