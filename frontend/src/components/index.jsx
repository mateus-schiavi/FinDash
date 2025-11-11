import { useEffect, useState } from "react";

function Index() {
    const [expenses, setExpenses] = uses([]);
    const [incomes, setIncomes] = uses([]);
    const [budgets, setBudgets] = uses([]);
    const [graphHtml, setGraphHtml] = uses([]);

    useEffect(() => {
        fetch("http://localhost:5000/api/data")
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    window.location.href = "/login";
                } else {
                    setExpenses(data.expenses);
                    setIncomes(data.incomes);
                    setBudgets(data.budgets);
                    setGraphHtml(data.graphHtml);
                }
            });
    }, []);

    useEffect(() => {
        if (graphHtml) {
            const graphDiv = document.getElementById("graph");
            graphDiv.innerHTML = graphHtml;
        }
    }, [graphHtml]);

    return(
        <>
        <div className="bg-gray-200 p-10">
            <h1 className="text-2xl mb-4 text-center">Dashboard Financeiro</h1>

            {/* Botões de download */}
            <div className="text-center mb-8">
                <a href="http://localhost:5000/download_data" className="btn btn-primary">
                    Baixar Dados em CSV
                </a>
                <a href="http://localhost:5000/download_data_xlsx" className="btn btn-primary">
                    Baixar Dados em EXCEL
                </a>
            </div>

            {/* Gráfico */}
            <div id="graph" className="mt-8"></div>

            {/* Formulários */}
            <AddIncomeForm />
            <AddExpenseForm />
            <AddBudgetForm />

            {/* Tabelas */}
            <ExpenseTable expenses={expenses}/>
            <Income Table incomes={incomes}/>
            <BudgetTable budget={budgets} />

            {/* Logout */}
            <div className="logout-container">
                <form action="http://localhost:5000/logout" method="post">
                <button type="submit" className="btn btn-logout mt-8 text-lg mb-2">
                    Sait
                </button>
                </form>
            </div>
        </div>
        </>
    )
}

export default Index;