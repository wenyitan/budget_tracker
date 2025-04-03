import axios from "axios";
import { useState, useEffect } from "react";

function TrancsactionTable() {

    const [ transactions, setTransactions ] = useState([]);

    const fetchTransactions = ()=> {
        axios.get("http://127.0.0.1:5000/transactions")
            .then((res) => {
                setTransactions(res.data);
            }).catch((err) => {
                console.log(err);
            })
    }

    useEffect(()=> {
        fetchTransactions();
    }, [])

    return (
        <table>
            <thead>
                <tr>
                    <th>No.</th>
                    <th>Date</th>
                    <th>Amount</th>
                    <th>Category</th>
                    <th>Description</th>
                    <th>Person</th>
                </tr>
            </thead>
            <tbody>
                {transactions.map((transaction, key)=> {
                    return (
                        <tr>
                            <th>{key}</th>
                            <th>{transaction.date}</th>
                            <th>{transaction.amount}</th>
                            <th>{transaction.category}</th>
                            <th>{transaction.description}</th>
                            <th>{transaction.person}</th>
                        </tr>
                    )
                })}
            </tbody>

        </table>
    )
};

export default TrancsactionTable;