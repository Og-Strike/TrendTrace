import subprocess
import os
import argparse

def install_requirements():
    try:
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
        print("Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing requirements: {e}")

def generate_mask(path,current_dir,name):
    # print("generate_mask start execute")
    output_dir = os.path.join(current_dir, "process.py")
    command = ["python", f'{output_dir}', "--image", f'{path}','--name_image',f'{name}']

    result = subprocess.run(command, capture_output=True, text=True)

    #Print the output and error (if any)
    print("Return code:", result.returncode)
    print("Output:")
    print(result.stdout)
    print("Error:")
    print(result.stderr)
    generatebound_from_mask(path,current_dir,name)

def generatebound_from_mask(path,current_dir,name):
    # print("generatebound start execute")
    output_dir = os.path.join(current_dir, "bbox.py")
    image_path = path
    name_image = name
    command = [
        "python", output_dir,  
        "--image", image_path,
        "--name_image", name_image
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    # Print the output and error (if any)
    # print("Return code:", result.returncode)
    print("Output:")
    print(result.stdout)
    print("Error:")
    print(result.stderr)



def main(args):
    #install_requirements()
    cwd = os.getcwd()
    generate_mask(args.image,cwd,args.name_image)
    # generate_mask(r'PATH',cwd,'testing1')

    if os.path.exists(args.image):
        os.remove(args.image)
    



    
if __name__ == '__main__':
    # print("Pipeline Execute")
    parser = argparse.ArgumentParser(description='Full Pipeline')
    parser.add_argument('--image', type=str, help='Path to the input image')
    parser.add_argument('--name_image',type=str,help='Name of file')
    args = parser.parse_args()
    main(args)


