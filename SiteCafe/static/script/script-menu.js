const { useState } = React;

function Menu() {
    const [itens, setItens] = useState([
        { 
            nome: "Café's", 
            preco: "R$ 6,00", 
            imagem: "/static/images/1.jpg",
            subItens: ["Cappuccino", "Café outro sla"]
        },
        { 
            nome: "Marmita Fit", 
            preco: "R$ 8,50", 
            imagem: "/static/images/2.jpeg",
            subItens: ["Marmita Frango", "Marmita Carne"] 
        },
        { 
            nome: "Salgados", 
            preco: "R$ 5,00", 
            imagem: "/static/images/3.png",
            subItens: ["Coxinha", "Pão de queijo"] 
        },
        { 
            nome: "Doces", 
            preco: "R$ 7,00", 
            imagem: "/static/images/4.png",
            subItens: ["Brigadeiro", "Beijinho"] 
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
                        <p className="p-menu">{item.preco}</p>
                        <span className="disponivel">Disponível ✅</span>

                        {expandido === index && (
                            <div className="sub-itens">
                                {item.subItens.map((subItem, i) => (
                                    <p key={i} className={`item${i + 1}`}>{subItem}</p>
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