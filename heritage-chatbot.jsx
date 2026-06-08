import { useState, useRef, useEffect } from "react";

const SITE_KNOWLEDGE = `
You are an expert guide for Mohenjo-daro, one of the world's most remarkable ancient cities and a UNESCO World Heritage Site located in Sindh, Pakistan.

KNOWLEDGE BASE:
- Location: Located on the right bank of the Indus River in Larkana District, Sindh, Pakistan. Coordinates: 27.3244° N, 68.1375° E
- Age & Period: Built around 2500 BCE during the Indus Valley Civilization (also called Harappan Civilization), flourishing until about 1900 BCE
- Name Meaning: "Mohenjo-daro" means "Mound of the Dead Men" in Sindhi
- Size: Covered approximately 250 hectares (620 acres), with an estimated population of 40,000–50,000 people
- Discovery: Rediscovered in 1922 by R. D. Banerji and later excavated by John Marshall and Ernest Mackay
- Architecture: Featured remarkably advanced urban planning — a grid-based street system, standardized fired brick construction, multi-story buildings, and public buildings
- The Great Bath: One of the earliest public water tanks in the ancient world (12m x 7m x 2.4m deep), possibly used for ritual bathing or civic ceremonies
- Drainage System: Sophisticated underground sewage and drainage system — arguably the world's first urban sanitation infrastructure
- The Granary: A large building believed to be a central granary for storing grain, indicating organized food distribution
- Assembly Hall: A pillared hall possibly used for public gatherings or administration
- The Dancing Girl: A famous bronze statuette (10.8 cm tall) of a young woman, now in the National Museum of India
- Priest-King: A steatite sculpture of a bearded figure wearing an ornamental robe, possibly depicting a religious or civic leader
- Writing System: The Indus script remains undeciphered — over 400 symbols found on seals and pottery
- Trade: Evidence of trade with Mesopotamia (modern Iraq), Central Asia, and other regions
- Decline: Reasons for decline debated — theories include climate change, Aryan invasion, flooding, or ecological degradation
- UNESCO Status: Inscribed as a World Heritage Site in 1980
- Preservation Issues: Waterlogging and salt crystallization are severely damaging the exposed ruins; UNESCO and Pakistani government are working on conservation
- Visitor Info: Open year-round; best visited October–March (cooler weather); nearest city is Larkana; archaeological museum on site
- Interesting Facts: No temples or palaces clearly identified; suggests a possible egalitarian or priest-led society; standardized weights and measures indicate regulated commerce

RESPONSE GUIDELINES:
- Answer questions about history, architecture, culture, daily life, decline, artifacts, visitor info, and preservation
- Be enthusiastic, educational, and engaging
- Provide vivid descriptions when asked about what the site looked like in the past
- Keep responses 2-4 paragraphs unless a short answer suffices
- Always be accurate to archaeological evidence
- End responses with a related follow-up question suggestion when appropriate
`;

const SAMPLE_QUESTIONS = [
  "What was daily life like in Mohenjo-daro?",
  "Tell me about the Great Bath",
  "Why did Mohenjo-daro decline?",
  "What artifacts were found here?",
  "How advanced was their architecture?",
  "What did the city look like 4,000 years ago?",
];

const IMAGE_PROMPTS = {
  default: "ancient Mohenjo-daro Indus Valley Civilization ruins archaeological site Pakistan",
  bath: "Great Bath Mohenjo-daro ancient water tank ruins archaeology",
  artifacts: "Mohenjo-daro Dancing Girl bronze statue ancient Indus artifact museum",
  city: "Mohenjo-daro ancient city reconstruction artist illustration Indus Valley",
  granary: "Mohenjo-daro granary ruins ancient storehouse archaeology",
  decline: "ancient Indus Valley Civilization decline flooding drought illustration",
  architecture: "Mohenjo-daro brick buildings ancient urban planning ruins aerial view",
  life: "Mohenjo-daro daily life ancient reconstruction illustration Indus people",
};

function getImageQuery(userMessage, botResponse) {
  const combined = (userMessage + " " + botResponse).toLowerCase();
  if (combined.includes("bath") || combined.includes("water")) return IMAGE_PROMPTS.bath;
  if (combined.includes("artifact") || combined.includes("statue") || combined.includes("dancing girl")) return IMAGE_PROMPTS.artifacts;
  if (combined.includes("look") || combined.includes("appear") || combined.includes("reconstruct")) return IMAGE_PROMPTS.city;
  if (combined.includes("granary") || combined.includes("grain") || combined.includes("food")) return IMAGE_PROMPTS.granary;
  if (combined.includes("decline") || combined.includes("fall") || combined.includes("end") || combined.includes("collapse")) return IMAGE_PROMPTS.decline;
  if (combined.includes("architect") || combined.includes("building") || combined.includes("brick") || combined.includes("street")) return IMAGE_PROMPTS.architecture;
  if (combined.includes("daily") || combined.includes("life") || combined.includes("people") || combined.includes("lived")) return IMAGE_PROMPTS.life;
  return IMAGE_PROMPTS.default;
}

async function askClaude(userMessage, history) {
  const messages = [
    ...history.map(m => ({ role: m.role, content: m.content })),
    { role: "user", content: userMessage }
  ];

  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1000,
      system: SITE_KNOWLEDGE,
      messages,
    }),
  });

  const data = await response.json();
  return data.content?.[0]?.text || "I couldn't generate a response. Please try again.";
}

async function fetchImage(query) {
  const UNSPLASH_QUERIES = {
    "ancient Mohenjo-daro Indus Valley Civilization ruins archaeological site Pakistan": "mohenjo daro ruins",
    "Great Bath Mohenjo-daro ancient water tank ruins archaeology": "ancient bath ruins archaeology",
    "Mohenjo-daro Dancing Girl bronze statue ancient Indus artifact museum": "ancient bronze artifact museum",
    "Mohenjo-daro ancient city reconstruction artist illustration Indus Valley": "ancient city ruins civilization",
    "Mohenjo-daro granary ruins ancient storehouse archaeology": "ancient ruins archaeology excavation",
    "ancient Indus Valley Civilization decline flooding drought illustration": "ancient ruins flood abandoned",
    "Mohenjo-daro brick buildings ancient urban planning ruins aerial view": "ancient brick ruins archaeological",
    "Mohenjo-daro daily life ancient reconstruction illustration Indus people": "ancient civilization people historical",
  };
  const search = UNSPLASH_QUERIES[query] || "ancient ruins archaeology";
  return `https://source.unsplash.com/800x450/?${encodeURIComponent(search)}&sig=${Math.random()}`;
}

export default function HeritageChatbot() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Welcome, traveler through time! 🏛️ I am your guide to **Mohenjo-daro** — one of the world's oldest and most sophisticated cities, built over 4,500 years ago along the Indus River in what is now Pakistan.\n\nAsk me anything about its history, architecture, daily life, mysterious decline, or plan your visit. What would you like to discover?",
      image: null,
      imageQuery: null,
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [imageLoading, setImageLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = async (text) => {
    const userText = text || input.trim();
    if (!userText || loading) return;
    setInput("");

    const userMsg = { role: "user", content: userText };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const history = messages.map(m => ({ role: m.role, content: m.content }));
      const reply = await askClaude(userText, history);
      const imgQuery = getImageQuery(userText, reply);

      setMessages(prev => [...prev, {
        role: "assistant",
        content: reply,
        image: null,
        imageQuery: imgQuery,
        loadingImage: true,
      }]);
      setLoading(false);

      // Load image
      setImageLoading(true);
      const imgUrl = await fetchImage(imgQuery);
      setMessages(prev => prev.map((m, i) =>
        i === prev.length - 1 ? { ...m, image: imgUrl, loadingImage: false } : m
      ));
      setImageLoading(false);

    } catch (err) {
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "I encountered an issue retrieving that information. Please try again.",
        image: null,
      }]);
      setLoading(false);
    }
  };

  const formatText = (text) => {
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br/>');
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(135deg, #0a0a0f 0%, #12100e 40%, #1a1208 100%)",
      fontFamily: "'Georgia', 'Times New Roman', serif",
      color: "#e8dcc8",
      display: "flex",
      flexDirection: "column",
    }}>
      {/* Decorative top pattern */}
      <div style={{
        background: "repeating-linear-gradient(90deg, #c9973a 0px, #c9973a 1px, transparent 1px, transparent 40px)",
        height: "3px",
        opacity: 0.6,
      }} />

      {/* Header */}
      <header style={{
        padding: "24px 32px",
        borderBottom: "1px solid rgba(201,151,58,0.25)",
        background: "rgba(0,0,0,0.4)",
        backdropFilter: "blur(10px)",
        display: "flex",
        alignItems: "center",
        gap: "20px",
        position: "sticky",
        top: 0,
        zIndex: 100,
      }}>
        <div style={{
          width: "52px", height: "52px",
          borderRadius: "50%",
          background: "linear-gradient(135deg, #c9973a, #8b5e1a)",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: "24px",
          boxShadow: "0 0 20px rgba(201,151,58,0.4)",
          flexShrink: 0,
        }}>🏛️</div>
        <div>
          <h1 style={{
            margin: 0,
            fontSize: "clamp(16px, 3vw, 22px)",
            fontWeight: "700",
            color: "#e8c87a",
            letterSpacing: "0.05em",
            textShadow: "0 0 30px rgba(201,151,58,0.5)",
          }}>MOHENJO-DARO</h1>
          <p style={{
            margin: "2px 0 0",
            fontSize: "12px",
            color: "#a08060",
            letterSpacing: "0.15em",
            textTransform: "uppercase",
          }}>Heritage AI Guide · Indus Valley Civilization · 2500 BCE</p>
        </div>
        <div style={{ marginLeft: "auto", display: "flex", gap: "8px", flexWrap: "wrap", justifyContent: "flex-end" }}>
          <span style={{
            background: "rgba(201,151,58,0.15)",
            border: "1px solid rgba(201,151,58,0.3)",
            borderRadius: "20px",
            padding: "4px 12px",
            fontSize: "11px",
            color: "#c9973a",
            letterSpacing: "0.1em",
          }}>🌍 UNESCO World Heritage</span>
          <span style={{
            background: "rgba(80,180,120,0.15)",
            border: "1px solid rgba(80,180,120,0.3)",
            borderRadius: "20px",
            padding: "4px 12px",
            fontSize: "11px",
            color: "#60c090",
            letterSpacing: "0.1em",
          }}>● AI Powered</span>
        </div>
      </header>

      {/* Chat Area */}
      <div style={{
        flex: 1,
        overflowY: "auto",
        padding: "32px 16px",
        maxWidth: "860px",
        width: "100%",
        margin: "0 auto",
        boxSizing: "border-box",
      }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{
            display: "flex",
            justifyContent: msg.role === "user" ? "flex-end" : "flex-start",
            marginBottom: "28px",
            animation: "fadeSlideIn 0.4s ease forwards",
          }}>
            {msg.role === "assistant" && (
              <div style={{
                width: "36px", height: "36px", borderRadius: "50%",
                background: "linear-gradient(135deg, #c9973a, #5a3a10)",
                display: "flex", alignItems: "center", justifyContent: "center",
                fontSize: "16px", flexShrink: 0, marginRight: "12px", marginTop: "4px",
                boxShadow: "0 2px 12px rgba(201,151,58,0.3)",
              }}>🏛️</div>
            )}

            <div style={{ maxWidth: "75%", minWidth: "120px" }}>
              {msg.role === "assistant" ? (
                <div style={{
                  background: "linear-gradient(135deg, rgba(30,22,10,0.95), rgba(20,15,8,0.98))",
                  border: "1px solid rgba(201,151,58,0.2)",
                  borderRadius: "4px 18px 18px 18px",
                  padding: "18px 22px",
                  boxShadow: "0 4px 20px rgba(0,0,0,0.4), inset 0 1px 0 rgba(201,151,58,0.1)",
                  lineHeight: "1.75",
                  fontSize: "15px",
                  color: "#d8ccb8",
                }}>
                  <div dangerouslySetInnerHTML={{ __html: `<p>${formatText(msg.content)}</p>` }}
                    style={{ margin: 0 }} />

                  {/* Image */}
                  {msg.loadingImage && (
                    <div style={{
                      marginTop: "16px",
                      height: "200px",
                      borderRadius: "10px",
                      background: "rgba(201,151,58,0.05)",
                      border: "1px solid rgba(201,151,58,0.15)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      gap: "8px",
                      color: "#a08060",
                      fontSize: "13px",
                    }}>
                      <span style={{ animation: "spin 1s linear infinite", display: "inline-block" }}>⟳</span>
                      Loading visual…
                    </div>
                  )}
                  {msg.image && (
                    <div style={{ marginTop: "16px" }}>
                      <img
                        src={msg.image}
                        alt="Heritage site visual"
                        style={{
                          width: "100%",
                          borderRadius: "10px",
                          border: "1px solid rgba(201,151,58,0.25)",
                          boxShadow: "0 8px 30px rgba(0,0,0,0.5)",
                          display: "block",
                        }}
                        onError={(e) => { e.target.style.display = "none"; }}
                      />
                      <p style={{
                        margin: "8px 0 0",
                        fontSize: "11px",
                        color: "#806040",
                        letterSpacing: "0.1em",
                        textTransform: "uppercase",
                      }}>📷 Related Visual · Mohenjo-daro</p>
                    </div>
                  )}
                </div>
              ) : (
                <div style={{
                  background: "linear-gradient(135deg, #c9973a, #a07020)",
                  borderRadius: "18px 4px 18px 18px",
                  padding: "14px 20px",
                  color: "#0a0800",
                  fontWeight: "600",
                  fontSize: "15px",
                  boxShadow: "0 4px 15px rgba(201,151,58,0.3)",
                  lineHeight: "1.6",
                }}>
                  {msg.content}
                </div>
              )}
            </div>

            {msg.role === "user" && (
              <div style={{
                width: "36px", height: "36px", borderRadius: "50%",
                background: "linear-gradient(135deg, #4a6080, #2a3a50)",
                display: "flex", alignItems: "center", justifyContent: "center",
                fontSize: "16px", flexShrink: 0, marginLeft: "12px", marginTop: "4px",
              }}>👤</div>
            )}
          </div>
        ))}

        {loading && (
          <div style={{ display: "flex", alignItems: "flex-start", marginBottom: "28px" }}>
            <div style={{
              width: "36px", height: "36px", borderRadius: "50%",
              background: "linear-gradient(135deg, #c9973a, #5a3a10)",
              display: "flex", alignItems: "center", justifyContent: "center",
              fontSize: "16px", marginRight: "12px",
            }}>🏛️</div>
            <div style={{
              background: "rgba(30,22,10,0.95)",
              border: "1px solid rgba(201,151,58,0.2)",
              borderRadius: "4px 18px 18px 18px",
              padding: "18px 22px",
              display: "flex", gap: "6px", alignItems: "center",
            }}>
              {[0,1,2].map(i => (
                <div key={i} style={{
                  width: "8px", height: "8px", borderRadius: "50%",
                  background: "#c9973a",
                  animation: `pulse 1.2s ease-in-out ${i * 0.2}s infinite`,
                }} />
              ))}
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Sample Questions */}
      <div style={{
        padding: "12px 16px 0",
        maxWidth: "860px",
        width: "100%",
        margin: "0 auto",
        boxSizing: "border-box",
      }}>
        <p style={{ margin: "0 0 8px", fontSize: "11px", color: "#806040", letterSpacing: "0.12em", textTransform: "uppercase" }}>
          Suggested questions:
        </p>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
          {SAMPLE_QUESTIONS.map((q, i) => (
            <button
              key={i}
              onClick={() => handleSend(q)}
              disabled={loading}
              style={{
                background: "rgba(201,151,58,0.08)",
                border: "1px solid rgba(201,151,58,0.25)",
                borderRadius: "20px",
                padding: "6px 14px",
                fontSize: "12px",
                color: "#c9a060",
                cursor: loading ? "not-allowed" : "pointer",
                transition: "all 0.2s",
                fontFamily: "inherit",
                opacity: loading ? 0.5 : 1,
              }}
              onMouseEnter={e => { if (!loading) { e.target.style.background = "rgba(201,151,58,0.2)"; e.target.style.color = "#e8c870"; }}}
              onMouseLeave={e => { e.target.style.background = "rgba(201,151,58,0.08)"; e.target.style.color = "#c9a060"; }}
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* Input Area */}
      <div style={{
        padding: "16px",
        maxWidth: "860px",
        width: "100%",
        margin: "0 auto",
        boxSizing: "border-box",
      }}>
        <div style={{
          display: "flex",
          gap: "12px",
          background: "rgba(20,15,8,0.9)",
          border: "1px solid rgba(201,151,58,0.3)",
          borderRadius: "16px",
          padding: "10px 10px 10px 20px",
          boxShadow: "0 4px 30px rgba(0,0,0,0.4), 0 0 0 1px rgba(201,151,58,0.05)",
        }}>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === "Enter" && !e.shiftKey && handleSend()}
            placeholder="Ask about Mohenjo-daro's history, architecture, artifacts, or your visit…"
            disabled={loading}
            style={{
              flex: 1,
              background: "transparent",
              border: "none",
              outline: "none",
              color: "#e8dcc8",
              fontSize: "15px",
              fontFamily: "inherit",
              lineHeight: "1.5",
            }}
          />
          <button
            onClick={() => handleSend()}
            disabled={loading || !input.trim()}
            style={{
              background: loading || !input.trim()
                ? "rgba(201,151,58,0.2)"
                : "linear-gradient(135deg, #c9973a, #a07020)",
              border: "none",
              borderRadius: "10px",
              width: "44px",
              height: "44px",
              cursor: loading || !input.trim() ? "not-allowed" : "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "18px",
              transition: "all 0.2s",
              flexShrink: 0,
            }}
          >
            {loading ? "⟳" : "↑"}
          </button>
        </div>
        <p style={{
          textAlign: "center",
          margin: "10px 0 0",
          fontSize: "11px",
          color: "#504030",
          letterSpacing: "0.05em",
        }}>
          Semester Project · Heritage Site AI · Mohenjo-daro, Sindh, Pakistan · 2500 BCE
        </p>
      </div>

      <style>{`
        @keyframes fadeSlideIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse {
          0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
          40% { opacity: 1; transform: scale(1); }
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        * { box-sizing: border-box; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: rgba(0,0,0,0.3); }
        ::-webkit-scrollbar-thumb { background: rgba(201,151,58,0.3); border-radius: 3px; }
        p { margin: 0 0 12px 0; }
        p:last-child { margin-bottom: 0; }
        strong { color: #e8c870; }
      `}</style>
    </div>
  );
}
