import React, { useState } from "react";

export default function AddIncomeForm() {
    const [formData, setFormData] = useState({
        description: "",
        value: "",
        date: "",
        source: "",
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        await fetch("http://localhost:5000/add_income", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData),
        }),
        alert("Renda adicionada!");
        setFormData({description: "", value: "", date: "", source: ""})
    };

    return (
        <>
        <form onSubmit={handleSubmit} className="mt-8">
            <h2 className="text-lg mb-2">Adicionar Renda</h2>
            <label>Descrição:</label>
            <input type="text" name="description" value={formData.description} onChange={handleChange} required className="form-input"/>

             <label>Valor:</label>
            <input type="text" name="description" value={formData.value} onChange={handleChange} required className="form-input"/>

             <label>Data:</label>
            <input type="text" name="description" value={formData.date} onChange={handleChange} required className="form-input"/>

             <label>Fonte:</label>
            <input type="text" name="description" value={formData.source} onChange={handleChange} required className="form-input"/>
        
            <button type="submit" className="btn">Adicionar Renda</button>
        </form>
        </>
    )
}