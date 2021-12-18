import React, { useState } from "react"
import { getContract, getContractStorage, wallet } from '../tezos';


import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

function Deposit(){

    const [modalIsOpen, setIsOpen] = useState(false);
    const [amt, setAmt] = useState("");
    

    function openModal(){
        setIsOpen(true);
    }

    function closeModal(){
        setIsOpen(false);
    }

    async function handleClick() {
        // Register here
        const activeAccount = await wallet.client.getActiveAccount();
        const contract = await getContract();
        const op =  await contract.methods.deposit(1).send({amount : amt});
		console.log(contract);
		
        await op.confirmation();
        alert("Deposit Successfully!")
        
    }

    return(
        <>
 <Modal
                show={modalIsOpen}
                onHide={closeModal}>
                <Modal.Body>
                    <Form.Group className="mb-3">
                        <Form.Label>Amount to Deposit</Form.Label>
                        <Form.Control 
                            type="text" 
                            placeholder="Amount in Tez " 
                            id="amt"
                            onChange={e => setAmt(e.target.value)}
                            value={amt}
                            classaddress="modal-input"/>
                    </Form.Group>

                   
                </Modal.Body>
                
                <Modal.Footer>
                    <Button variant="secondary" onClick={closeModal}>Close</Button>
                    <Button variant="primary" onClick={handleClick} className="modal-submit-btn">Submit</Button>
                </Modal.Footer>
            </Modal>

                   
            <h3 className="header-h3" onClick={openModal} >Deposit</h3>
        </>
    );
};

function Stake(){

    const [modalIsOpen, setIsOpen] = useState(false);
   const [amt, setAmt] = useState("");
    

    function openModal(){
        setIsOpen(true);
    }

    function closeModal(){
        setIsOpen(false);
    }

    async function handleClick() {
        // Register here
        const activeAccount = await wallet.client.getActiveAccount();
		console.log(activeAccount.address);
        const contract = await getContract();
        const op =  await contract.methods.addStake(1).send({amount : amt});
        await op.confirmation();
        alert("Stake Added!")
        
    }

    return(
        <>
            <Modal
                show={modalIsOpen}
                onHide={closeModal}>
                <Modal.Body>
                    <Form.Group className="mb-3">
                        <Form.Label>Amount to Stake</Form.Label>
                        <Form.Control 
                            type="text" 
                            placeholder="Amount in Tez " 
                            id="amt"
                            onChange={e => setAmt(e.target.value)}
                            value={amt}
                            classaddress="modal-input"/>
                    </Form.Group>

                   
                </Modal.Body>
                
                <Modal.Footer>
                    <Button variant="secondary" onClick={closeModal}>Close</Button>
                    <Button variant="primary" onClick={handleClick} className="modal-submit-btn">Submit</Button>
                </Modal.Footer>
            </Modal>
            <h3 className="header-h3" onClick={openModal} >Stake</h3>
        </>
    );
}

export {Deposit, Stake};
