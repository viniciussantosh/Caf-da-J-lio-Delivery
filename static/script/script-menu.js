const { useState } = React;

function Menu() {
    const [itens, setItens] = useState([
    {
        nome: "Café's",
        imagem: "/static/images/cafes.jpg",
        subItens: [
            { nome: "Cappuccino", preco: "R$ 6,00", descricao: "Café cremoso com leite vaporizado e chocolate." },
            { nome: "Café Expresso", preco: "R$ 5,00", descricao: "Café forte e encorpado." },
            { nome: "Café Coado", preco: "R$ 4,50", descricao: "Tradicional café coado." },
            { nome: "Café Gelado", preco: "R$ 8,00", descricao: "Café gelado com leite e cubos de gelo." },
            { nome: "Mocha", preco: "R$ 7,50", descricao: "Café com chocolate e chantilly." }
        ]
    },
    {
        nome: "Marmita Fit",
        imagem: "/static/images/2.jpeg",
        subItens: [
            { nome: "Marmita Frango", preco: "R$ 8,50", descricao: "Frango grelhado com legumes." },
            { nome: "Marmita Carne", preco: "R$ 9,00", descricao: "Carne assada com arroz integral." },
            { nome: "Marmita Vegetariana", preco: "R$ 8,00", descricao: "Legumes grelhados com quinoa." },
            { nome: "Marmita Peixe", preco: "R$ 10,00", descricao: "Filé de peixe com batata doce." },
            { nome: "Marmita Low Carb", preco: "R$ 9,50", descricao: "Opção com baixo teor de carboidratos." }
        ]
    },
    {
        nome: "Salgados",
        imagem: "/static/images/salgados.jpeg",
        subItens: [
            { nome: "Coxinha", preco: "R$ 5,00", descricao: "Coxinha crocante recheada com frango." },
            { nome: "Pão de queijo", preco: "R$ 3,00", descricao: "Pão de queijo quentinho e saboroso." },
            { nome: "Empada", preco: "R$ 4,50", descricao: "Empada de frango ou palmito." },
            { nome: "Pastel", preco: "R$ 6,00", descricao: "Pastel assado com diversos recheios." },
            { nome: "Esfiha", preco: "R$ 3,50", descricao: "Esfiha aberta de carne ou queijo." }
        ]
    },
    {
        nome: "Doces",
        imagem: "/static/images/item.jpeg",
        subItens: [
            { nome: "Brigadeiro", preco: "R$ 2,00", descricao: "Doce tradicional de chocolate." },
            { nome: "Beijinho", preco: "R$ 2,00", descricao: "Doce de coco com leite condensado." },
            { nome: "Brownie", preco: "R$ 4,50", descricao: "Brownie de chocolate com nozes." },
            { nome: "Torta de Limão", preco: "R$ 5,00", descricao: "Torta cremosa de limão." },
            { nome: "Pudim", preco: "R$ 4,00", descricao: "Pudim tradicional de leite condensado." }
        ]
    }
]);

    const [expandido, setExpandido] = useState(null);

    const handleExpandir = (index) => {
        setExpandido(expandido === index ? null : index);
    };

    return (
        <div className="menu-section">
            <h2 className="menu-title">Nosso Cardápio ☕</h2>
            <div className="menu-grid">
                {itens.map((item, index) => (
                    <div
                        key={index}
                        className={`menu-item ${expandido === index ? "expandido" : ""}`}
                        onClick={() => handleExpandir(index)}
                    >
                        <img src={item.imagem} alt={item.nome} className="img-menu"/>
                        <h3 className="h3-menu">{item.nome}</h3>

                        {expandido === index && (
                            <div className="sub-itens">
                                {item.subItens.map((subItem, i) => (
                                    <a
                                        href={`/item/${encodeURIComponent(subItem.nome)}`}
                                        key={i}
                                    >
                                        <p className={`item${i + 1}`}>
                                            {subItem.nome} - {subItem.preco}
                                        </p>
                                    </a>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}

ReactDOM.createRoot(document.getElementById("root")).render(<Menu />);
