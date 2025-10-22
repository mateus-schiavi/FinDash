import "../../src/index.css";
import { useState } from "react";
import { Link } from "react-router-dom";

function Register({ onRegister, errorMessage }) {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onRegister(formData); // função que você define depois
  };

  return (
    <div className="login-container">
      <img
        src="https://cdn.freelogodesign.org/files/d70543f13825477d997d8554226d4e34/thumb/logo_200x200.png?v=638460380530000000"
        alt="Logo do software Cadê meu caixa?"
      />

      <h1>Cadastre-se</h1>

      {errorMessage && <p className="error-message">{errorMessage}</p>}

      <form onSubmit={handleSubmit}>
        <label htmlFor="name">Nome de Usuário:</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />

        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />

        <label htmlFor="password">Senha:</label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />

        <button type="submit">Registrar</button>
      </form>

      <p>
        Já possui uma conta?{" "}
        <Link to="/">Realize o login aqui!</Link>
      </p>
    </div>
  );
}

export default Register;
