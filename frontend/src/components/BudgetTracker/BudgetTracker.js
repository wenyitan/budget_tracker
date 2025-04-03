import TrancsactionTable from "./TransactionTable/TransactionTable";
import "./BudgetTracker.css"

function BudgetTracker() {
    return (
        <div className="col-container">
            <h1>Budget Tracker</h1>
            <div className="container">
                <TrancsactionTable/>
                {/* <TrancsactionTable/> */}
            </div>
        </div>
    )

}

export default BudgetTracker;