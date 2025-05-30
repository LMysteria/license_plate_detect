import React, { useState } from "react";
import { getBackendContext } from "../Util/AuthUtil";

const DetectLicense = () => {
    // Define a functional component named UploadAndDisplayImage
    const UploadAndDisplayImage = () => {
    console.log("reloaded")
    // Define a state variable to store the selected image
    const [selectedImage, setSelectedImage] = useState(null);
    const [license, setLicense] = useState(null);

    const fetching = (img) => {
    const form = new FormData()
    form.append("img",img)
    console.log(img.type)
    console.log(form)
    fetch(`${getBackendContext()}/detect`,{
        method: "POST",
        body: form
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        let result = ""
        for (let i in data["license_number"]){
        result += data["license_number"][i] + ", "
        }
        setLicense(result)
    })
    .catch((err)=>console.log(err))
    }
    
    // Return the JSX for rendering
    return (
        <div>
        {/* Header */}
        <h1>Upload Image to detect License Number</h1>
    
        {/* Conditionally render the selected image if it exists */}
        {selectedImage&&(
            <div>
            {/* Display the selected image */}
            <img
                alt="not found"
                width={"250px"}
                src={URL.createObjectURL(selectedImage)}
            />
            <br/>
            <p>{license}</p>
            <br /> <br />
            {/* Button to remove the selected image */}
            <button onClick={() => {setSelectedImage(null); setLicense(null)}}>Remove</button>
            </div>
        )}
    
        <br />
        {/* Input element to select an image file */}
        <input
            type="file"
            name="img"
            // Event handler to capture file selection and update the state
            onChange={(event) => {
            console.log(event.target.files[0]); // Log the selected file
            setSelectedImage(event.target.files[0]); // Update the state with the selected file
            setLicense("detecting license...")
            fetching(event.target.files[0])
            }}
        />
        <br/>
        
        </div>
    );

    
    };

    return UploadAndDisplayImage()
}

export default DetectLicense;