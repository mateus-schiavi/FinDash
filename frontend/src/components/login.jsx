import "../../src/index.css";
import { useState } from "react";

function Login({ onLogin, errorMessage }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin({ username, password });
  };

  return (
    <div className="login-container">
      <img
        src="https://cdn.freelogodesign.org/files/d70543f13825477d997d8554226d4e34/thumb/logo_200x200.png?v=638460380530000000"
        alt="Logo do software Cadê meu caixa?"
      />
      <h1>Login</h1>

      {errorMessage && <p className="error-message">{errorMessage}</p>}

      <form onSubmit={handleSubmit}>
        <label htmlFor="username">Nome de Usuário:</label>
        <input
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <label htmlFor="password">Senha:</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <div className="flex-between">
          <button type="submit">Login</button>
        </div>
      </form>

      <p>
        Não lembra sua senha? <a href="/reset-password">Redefinir Senha</a>
      </p>
      <p>
        Não possui uma conta? <a href="/register">Cadastre-se aqui!</a>
      </p>
    </div>
  );
}

export default Login;
