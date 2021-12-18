import React, { useState } from 'react';
import { getActiveAccount, clearActiveAccount } from "../tezos";
import Login from "../images/login.png";
import "../App.css";

function LoginButton(){

    const [walletConnected, setWalletConnected] = useState(false);

    const handleLogin = async () => {
        // Login/Logout here
        if(!walletConnected) {
        	let activeAccount = await getActiveAccount();
        	setWalletConnected(true);
        	console.log(activeAccount);
        } else {
        	await clearActiveAccount();
        	setWalletConnected(false);
        }
        
    }

    return(
        <>

           <h3 className="header-h3" onClick={handleLogin} >
               {walletConnected ? ('Logout') : ('Login')}
            </h3>
        </>
    );
}

export default LoginButton;
