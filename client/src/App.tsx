import { useState } from 'react';
import Home from './components/Home';
import Chat from './components/Chat';



const App = () => {
  const [route, setRoute] = useState<"home" | "chat">("home");

  return (
    <div className="h-screen bg-zinc-950 text-zinc-100">
      {route === "home" ? (
        <Home onStart={() => setRoute("chat")} />
      ) : (
        <Chat onBack={() => setRoute("home")} />
      )}
    </div>
  );
}

export default App
