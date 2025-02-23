// Seleciona os formulários

const API_URL = "http://localhost:8000"; 

const formAluno = document.getElementById("formAluno");
const formPlano = document.getElementById("formPlano");
const formConsultarAluno = document.getElementById("formConsultarAluno");
const formConsultarPlano = document.getElementById("formConsultarPlano");
// Função para exibir o formulário correto
function exibirFormulario(formularioId) {
   const formularios = document.querySelectorAll(".formulario");
   formularios.forEach((formulario) => {
       formulario.classList.remove("ativo");
   });
   document.getElementById(formularioId).classList.add("ativo");
}
// Cadastro de Aluno
formAluno.addEventListener("submit", async (event) => {
   event.preventDefault();
   const aluno = {

    nome: document.getElementById("nome").value,
    idade: parseInt(document.getElementById("idade").value),
    plano_id: parseInt(document.getElementById("plano").value),

   };
   try {
       const response = await fetch("http://127.0.0.1:8000/alunos/", {
           method: "POST",
           headers: { "Content-Type": "application/json" },
           body: JSON.stringify(aluno),
       });
       alert(response.ok ? "Aluno cadastrado com sucesso!" : "Erro ao cadastrar aluno.");
       formAluno.reset();
   } catch (error) {
       alert("Erro ao cadastrar aluno.");
   }
});


// Consulta de Aluno por Nome
document.getElementById("formConsultarAluno").addEventListener("submit", async function (event) {
    event.preventDefault(); // Impede o recarregamento da página

    // Captura o valor do campo de entrada do nome
    const alunoNome = document.getElementById("consultaNomeAluno").value.trim();

    // Verifica se o nome foi preenchido
    if (!alunoNome) {
        alert("Por favor, insira o nome do aluno.");
        return;
    }

    try {
        // Faz a requisição para o backend
        const response = await fetch(`http://127.0.0.1:8000/alunos?nome=${encodeURIComponent(alunoNome)}`);

        // Verifica se a resposta é válida
        if (!response.ok) {
            throw new Error("Aluno não encontrado ou erro na consulta.");
        }

        // Converte a resposta para JSON
        const aluno = await response.json();

        // Exibe o resultado no HTML
        const resultadoDiv = document.getElementById("resultadoConsultaAluno");
        resultadoDiv.innerHTML = `
            <h3>Aluno Encontrado</h3>
            <p><strong>ID:</strong> ${aluno.id}</p>
            <p><strong>Nome:</strong> ${aluno.nome}</p>
            <p><strong>Idade:</strong> ${aluno.idade}</p>
            <p><strong>Plano:</strong> ${aluno.plano_id}</p>
        `;
    } catch (error) {
        // Trata erros e exibe uma mensagem para o usuário
        console.error(error.message);
        alert("Erro ao consultar aluno. Verifique o nome e tente novamente.");
    }
});
 
// Função para consultar todos os planos
async function consultarPlano() {
    try {
        const response = await fetch(`${API_URL}/planos`);
        if (!response.ok) {
            throw new Error("Erro ao consultar planos");
        }
        const planos = await response.json();
        
        // Exibe os planos no HTML (adiciona à div resultadoConsultaPlano)
        const resultadoConsultaPlano = document.getElementById("resultadoConsultaPlano");
        resultadoConsultaPlano.innerHTML = "";  // Limpa a div antes de adicionar os planos
        
        if (planos.length === 0) {
            resultadoConsultaPlano.textContent = "Nenhum plano encontrado.";
        } else {
            planos.forEach(plano => {
                const planoDiv = document.createElement("div");
                planoDiv.classList.add("plano-item");
                planoDiv.innerHTML = `<strong>Plano ID: ${plano.id} | <strong>Plano:</strong> ${plano.tipo} - <strong>Preço:</strong> R$ ${plano.preco}`;
                resultadoConsultaPlano.appendChild(planoDiv);
            });
        }
    } catch (error) {
        alert("Erro ao consultar planos: " + error.message);
    }
}

// Chama a função para consultar todos os planos quando o botão for clicado
const btnConsultarPlano = document.getElementById("btnConsultarPlano");
if (btnConsultarPlano) {
    btnConsultarPlano.addEventListener("click", consultarPlano);
}


