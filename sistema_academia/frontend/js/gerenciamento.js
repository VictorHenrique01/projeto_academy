// Alterna entre os forms
function mostrarSecao(secaoId) {
    const secoes = document.querySelectorAll('.secao-gerenciamento');
    secoes.forEach(secao => secao.classList.remove('ativa'));
    const secaoSelecionada = document.getElementById(secaoId);
    secaoSelecionada.classList.add('ativa');
 }
 

 document.addEventListener("DOMContentLoaded", function () {
    const equipamentosPorTreino = {
        "Membros Inferiores": ["Leg Press", "Cadeira Extensora", "Cadeira Flexora"],
        "Membros Superiores": ["Supino", "Pulley", "Máquina de Peito"],
        "Costas e Bíceps": ["Remada Baixa", "Halteres", "Pulley"],
        "Peito e Tríceps": ["Supino", "Polia", "Barras"],
        "Quadríceps": ["Cadeira Extensora", "Barra Guiada Smith", "Halteres", "Bancos para Musculação"],
        "Pernas Completo": ["Leg Press", "Cadeira Flexora", "Cadeira Abdutora"],
        "Ombros e Abdômen": ["Abdominal Máquina", "Halteres", "Máquina Ombro"],
        "Corpo Inteiro": ["Anilhas", "Halteres", "Mesa Posterior", "Leg Press 45 graus", "Bancos para Musculação"],
        "Cardio": ["Esteira", "Bicicleta Ergométrica"],
        "Flexibilidade": ["Colchonetes para Alongamento", "Bola de Pilates", "Elásticos de Resistência"]
    };

    const tipoTreinoSelect = document.getElementById("tipoTreino");
    const equipamentosSugeridosDiv = document.getElementById("equipamentosSugeridos");

    tipoTreinoSelect.addEventListener("change", function () {
        const tipoSelecionado = tipoTreinoSelect.value;
        const equipamentos = equipamentosPorTreino[tipoSelecionado] || [];

        if (equipamentos.length > 0) {
            equipamentosSugeridosDiv.innerHTML = `
                <label>Equipamentos Sugeridos ao Treino escolhido:</label>
                <ul>${equipamentos.map(equip => `<li>${equip}</li>`).join("")}</ul>
            `;
            equipamentosSugeridosDiv.style.display = "block"; // Mostra a seção
        } else {
            equipamentosSugeridosDiv.style.display = "none"; // Esconde se não tiver equipamentos
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const instrutoresPorTurma = {
        "Boxe": ["Netinho"],
        "Natação": ["Sheila", "Renan"],
        "Pilates": ["Luana", "Tatiane"]
    };

    const periodosInstrutores = {
        "Sheila": { inicio: "14:00", fim: "18:00" },  
        "Renan": { inicio: "08:00", fim: "12:00" },   
        "Netinho": { inicio: "18:00", fim: "22:00" }, 
        "Luana": { inicio: "18:00", fim: "22:00" },   
        "Tatiane": { inicio: "08:00", fim: "12:00" }  
    };

    const nomeTurmaSelect = document.getElementById("nomeTurma");
    const instrutorTurmaSelect = document.getElementById("instrutorTurma");
    const horarioInput = document.getElementById("horario");
    const botaoConsulta = document.getElementById("botaoConsulta");

    function atualizarInstrutores() {
        const turmaSelecionada = nomeTurmaSelect.value;
        instrutorTurmaSelect.innerHTML = ""; 

        if (turmaSelecionada && instrutoresPorTurma[turmaSelecionada]) {
            instrutoresPorTurma[turmaSelecionada].forEach(instrutor => {
                const option = document.createElement("option");
                option.value = instrutor;
                option.textContent = instrutor;
                instrutorTurmaSelect.appendChild(option);
            });
        } else {
            const option = document.createElement("option");
            option.value = "";
            option.textContent = "Selecione uma turma primeiro";
            instrutorTurmaSelect.appendChild(option);
        }
    }

    function validarHorario() {
        const instrutorSelecionado = instrutorTurmaSelect.value;
        const horarioSelecionado = horarioInput.value;

        if (instrutorSelecionado && horarioSelecionado) {
            const { inicio, fim } = periodosInstrutores[instrutorSelecionado];

            if (horarioSelecionado < inicio || horarioSelecionado > fim) {
                alert(`⚠️ Profissional ${instrutorSelecionado} só dá aulas entre ${inicio} e ${fim}. Consulte a disponibilidade de instrutor(a) e escolha um horário válido.`);
                horarioInput.value = ""; 

                // Exibe o botão caso o horário seja inválido
                botaoConsulta.style.display = "block";
            } else {
                // Oculta o botão se o horário for válido
                botaoConsulta.style.display = "none";
            }
        }
    }

    async function consultarDisponibilidade() {

        try {
            const response = await fetch(`/instrutores/${periodo}`);
            const data = await response.json();

            if (data.instrutores && data.instrutores.length > 0) {
                alert(`Instrutores disponíveis no período ${periodo}: \n` + data.instrutores.map(i => `- ${i.nome} (Especialidade: ${i.especialidade})`).join("\n"));
            } else {
                alert(`Nenhum instrutor disponível no período ${periodo}.`);
            }
        } catch (error) {
            console.error("Erro ao consultar disponibilidade:", error);
            alert("Erro ao consultar disponibilidade. Tente novamente.");
        }
    }

    botaoConsulta.addEventListener("click", consultarDisponibilidade);
    nomeTurmaSelect.addEventListener("change", atualizarInstrutores);
    horarioInput.addEventListener("change", validarHorario);
});



