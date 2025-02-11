from flask import Flask, request, jsonify
from deepface import DeepFace
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/verify', methods=['POST'])
def verify_faces():
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({"error": "Both images are required"}), 400

    image1 = request.files['image1']
    image2 = request.files['image2']

    if not allowed_file(image1.filename) or not allowed_file(image2.filename):
        return jsonify({"error": "Invalid file type. Only png, jpg, jpeg are allowed."}), 400

    if not os.path.exists('temp'):
        os.makedirs('temp')

    image1_path = os.path.join('temp', secure_filename(image1.filename))
    image2_path = os.path.join('temp', secure_filename(image2.filename))

    image1.save(image1_path)
    image2.save(image2_path)

    try:
        result = DeepFace.verify(image1_path, image2_path, distance_metric='euclidean_l2')
        print("*********RESULT**********", result)

        distance = result['distance']
        threshold = result['threshold']
        similarity_percentage = (1 - (distance / threshold)) * 100

        if result["verified"]:
            response = {
                "message": "Both images show the same person.",
                "distant": distance,
                "threshold": threshold,
                "confidence": f"{similarity_percentage:.2f}%"
            }
        else:
            response = {
                "message": "The images do not show the same person.",
                "distant": distance,
                "threshold": threshold,
                "confidence": f"{similarity_percentage:.2f}%"
            }

    except Exception as e:
        return jsonify({"error": f"An error occurred while verifying faces: {str(e)}"}), 500

    finally:
        os.remove(image1_path)
        os.remove(image2_path)

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
