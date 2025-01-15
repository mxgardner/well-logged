import React, { useState } from 'react';
import myImage from './blockchain.png';

const InputMenu = () => {
    const [input1, setInput1] = useState('');
    const [input2, setInput2] = useState('');
    const [input3, setInput3] = useState('');
    const [image, setImage] = useState(null);

    const handleSubmit = () => {
        if (input1.trim() === "" || input2.trim() === "" || input3.trim() === "") {
            alert("Please enter valid inputs.");
            return;
        }

        // Set the image to the local image
        setImage(myImage);  // Use the imported image

        setTimeout(() => {
            alert("Processing successful.");
        }, 5500);

        alert("Processing successful.");
    };

    return (
        <div className="input-menu">
            <h3>Enter Your Strings</h3>
            <input 
                type="text" 
                placeholder="Contract Address" 
                value={input1} 
                onChange={(e) => setInput1(e.target.value)}  
                style={{ padding: '8px', width: '100%', marginBottom: '10px' }}
            />
            <input 
                type="text" 
                placeholder="IPFS Hash" 
                value={input2} 
                onChange={(e) => setInput2(e.target.value)}  
                style={{ padding: '8px', width: '100%', marginBottom: '10px' }}
            />
            <input 
                type="text" 
                placeholder="Ethereum Address" 
                value={input3} 
                onChange={(e) => setInput3(e.target.value)}  
                style={{ padding: '8px', width: '100%', marginBottom: '10px' }}
            />
            <button onClick={handleSubmit} style={{ padding: '10px', cursor: 'pointer' }}>
                Submit
            </button>

            {/* Display the image if available */}
            {image && (
                <div style={{ marginTop: '20px' }}>
                    <img src={image} alt="Demo Result" style={{ maxWidth: '100%' }} />
                </div>
            )}
        </div>
    );
};

export default InputMenu;
