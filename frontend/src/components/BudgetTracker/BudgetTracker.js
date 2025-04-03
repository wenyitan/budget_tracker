import TrancsactionTable from "./TransactionTable/TransactionTable";

function BudgetTracker() {
    return (
        <div>
            <h1>Budget Tracker</h1>
            <div className="container">
                <TrancsactionTable/>
                <TrancsactionTable/>
            </div>
        </div>
    )

}

export default BudgetTracker;