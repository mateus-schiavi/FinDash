// src/components/Login.jsx
import React, { useState } from "react";

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Exemplo de chamada para sua API Django
    const response = await fetch("/api/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          localStorage.setItem("access_token", data.access);
          localStorage.setItem("refresh_token", data.refresh);
          window.location.href = "/dashboard";
        } else {
          setError(data.error);
        }
      });


    if (response.ok) {
      const data = await response.json();
      onLogin(data); // callback para atualizar estado de login no React
    } else {
      setError("Nome ou senha inválidos");
    }
  };

  return (
    <div className="bg-gray-900 flex justify-center items-center h-screen">
      <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <img
          className="h-auto max-w-lg mx-auto"
          src="https://cdn.freelogodesign.org/files/d70543f13825477d997d8554226d4e34/thumb/logo_200x200.png?v=638460380530000000"
          alt="Logo do software Cadê meu caixa?"
        />
        <h1 className="text-2xl mb-4">Login</h1>

        {error && <p className="text-red-600">{error}</p>}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label
              htmlFor="username"
              className="block text-gray-700 text-sm font-bold mb-2"
            >
              Nome de Usuário:
            </label>
            <input
              type="text"
              id="username"
              name="username"
              className="border-gray-400 border p-2 w-full"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          <div className="mb-6">
            <label
              htmlFor="password"
              className="block text-gray-700 text-sm font-bold mb-2"
            >
              Senha:
            </label>
            <input
              type="password"
              id="password"
              name="password"
              className="border-gray-400 border p-2 w-full"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <div className="flex items-center justify-between">
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Login
            </button>
          </div>
        </form>

        <p className="mt-4">
          Não lembra sua senha?
          <a href="/reset-password" className="text-blue-500">
            {" "}
            Redefinir Senha
          </a>
        </p>

        <p className="mt-4">
          Não possui uma conta?
          <a href="/register" className="text-blue-500">
            {" "}
            Cadastre-se aqui!
          </a>
        </p>
      </div>
    </div>
  );
}
