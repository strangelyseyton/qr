import qrcode
from PIL import Image

# Function to get vCard information
def get_vcard_info():
    print("Enter vCard information:")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    organization = input("Organization: ")
    title = input("Title: ")
    phone = input("Phone Number (e.g., (123) 456-7890): ")
    email = input("Email: ")
    url = input("URL: ")

    return f"""
BEGIN:VCARD
VERSION:3.0
N:{last_name};{first_name}
FN:{first_name} {last_name}
ORG:{organization}
TITLE:{title}
TEL;TYPE=WORK,VOICE:{phone}
EMAIL;TYPE=PREF,INTERNET:{email}
URL:{url}
END:VCARD
""", f"{first_name}_{last_name}"

# Function to get formatting preferences
def get_formatting_preferences():
    print("\nEnter QR code formatting preferences:")
    fill_color = input("Fill color (e.g., black): ")
    back_color = input("Background color (e.g., white): ")
    box_size = int(input("Box size (e.g., 10): "))
    border = int(input("Border size (e.g., 4): "))

    return fill_color, back_color, box_size, border

# Function to add logo to the QR code
def add_logo(qr_code, logo_path):
    logo = Image.open(logo_path)
    qr_box = qr_code.size
    logo_size = qr_box[0] // 4  # Logo size is 1/4th of the QR code size
    logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)
    
    # Calculate coordinates to place the logo at the center
    pos = ((qr_box[0] - logo_size) // 2, (qr_box[1] - logo_size) // 2)
    qr_code.paste(logo, pos, mask=logo)

# Get user input for vCard and formatting
vcard, fullname = get_vcard_info()
fill_color, back_color, box_size, border = get_formatting_preferences()

# Create qr code instance
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=box_size,
    border=border,
)

# Add data
qr.add_data(vcard)
qr.make(fit=True)

# Create an image from the QR Code instance
qr_code_img = qr.make_image(fill_color=fill_color, back_color=back_color)

# Ask user if they want to add a logo
add_logo_option = input("\nDo you want to add a logo to the QR code? (yes/no): ").lower()
if add_logo_option == 'yes':
    logo_path = input("Enter path to the company logo: ")
    add_logo(qr_code_img, logo_path)

# Save the QR code in the same directory as the program
file_name = f"{fullname}_qr.png".replace(" ", "_")
qr_code_img.save(file_name)

print(f"\nQR Code saved as {file_name}")
