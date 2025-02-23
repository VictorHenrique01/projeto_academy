const API_URL = "http://localhost:8000";

// Função para exibir formulários
function exibirFormulario(formularioId) {
    document.querySelectorAll(".formulario").forEach(form => form.classList.remove("ativo"));
    document.getElementById(formularioId).classList.add("ativo");
}

// Função para consultar todos os planos
async function consultarPlanos() {
    try {
        const response = await fetch(`${API_URL}/planos`);
        if (!response.ok) {
            throw new Error("Erro ao consultar planos");
        }
        const planos = await response.json();
        
        
        const resultadoConsultaPlano = document.getElementById("resultadoConsultaPlano");
        resultadoConsultaPlano.innerHTML = "";  // Limpa a div antes de add os planos
        
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

// Chama a função para consultar tds os planos qnd o botão for clicado
const btnConsultarPlano = document.getElementById("btnConsultarPlano");
if (btnConsultarPlano) {
    btnConsultarPlano.addEventListener("click", consultarPlanos);
}


async function trocarPlanoAluno() {
    console.log("Função trocarPlanoAluno foi chamada!");  // Teste
    try {
        const alunoId = document.getElementById("idAluno").value;
        const novoPlanoId = document.getElementById("novoPlanoId").value;
        
        console.log(`ID do Aluno: ${alunoId}, Novo Plano ID: ${novoPlanoId}`);  // Teste

        const response = await fetch(`${API_URL}/alunos/${alunoId}/trocar-plano`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ novo_plano_id: novoPlanoId })
        });

        console.log("Requisição enviada..."); // Teste
        
        const data = await response.json();
        alert(data.mensagem);
    } catch (error) {
        console.error("Erro ao trocar plano:", error); // Teste
        alert("Erro ao trocar plano do aluno: " + error.message);
    }
}

const btnTrocarPlano = document.getElementById("btnTrocarPlano");
if (btnTrocarPlano) {
    console.log("Botão encontrado e evento adicionado!"); // Teste
    btnTrocarPlano.addEventListener("click", trocarPlanoAluno);
} else {
    console.error("Botão NÃO encontrado!"); // Teste
}


// Consultar Equipamento
const formConsultarEquipamento = document.getElementById("formConsultarEquipamento");
if (formConsultarEquipamento) {
    formConsultarEquipamento.addEventListener("submit", async (event) => {
        event.preventDefault();
        const nome = document.getElementById("consultaNomeEquipamento").value;
        const resultadoDiv = document.getElementById("resultadoConsultaEquipamento");

        try {
            const response = await fetch(`${API_URL}/equipamentos/${nome}`);
            if (!response.ok) {
                throw new Error("Erro ao buscar equipamento");
            }

            const data = await response.json();
            console.log("Resposta da API:", data); 

            // dados retornados
            if (data && data.nome) {
                resultadoDiv.innerHTML = `
                    <p><strong>Nome:</strong> ${data.nome}</p>
                    <p><strong>Quantidade de ${data.nome} na academia:</strong> ${data.quantidade}</p>
                    <p><strong>Última manutenção feita:</strong> ${data.manutencao}</p>`;

                    botaoManutencao.style.display = "block"
                    botaoManutencao.addEventListener("click", function(){
                        alert("Solicitação será encaminhada em breve...");
                    })
                    ;
            } else {
                resultadoDiv.innerHTML = `<p>Equipamento não encontrado.</p>`;
                botaoManutencao.style.display = "none"; 
            }
        } catch (error) {
            resultadoDiv.innerHTML = `<p style="color: red;">Erro ao consultar equipamento.</p>`;
            botaoManutencao.style.display = "none"; 
        }
    });
}
