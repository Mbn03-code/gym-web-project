import { Toaster } from "react-hot-toast";
import AppRoutes from "./routes/AppRoutes.jsx";

function App() {
  return (
    <>
      <AppRoutes />

      
      <Toaster
        position="top-center"
        toastOptions={{
          duration: 3600,
          style: {
            direction: "rtl",
            fontFamily: "CafeYabYekan, Tahoma, sans-serif",
            color: "#6B4E3D",
            background: "#FFF5EB",
            border: "1px solid #F6E6CE",
          },
        }}
      />
    </>
  );
}

export default App;
