import Login from "./pages/Login";
import Home from "./pages/Home";
import NotFound from "./pages/NotFound";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import "./App.css";
import ProtectedRoute from "./components/ProtectedRoute";
import Watchlist from "./pages/watchlist";

function Logout() {
  localStorage.clear();
  return <Navigate to="/login"></Navigate>;
}

function RegisterAndLogout() {
  localStorage.clear();
  return <Navigate to="/signup"></Navigate>;
}

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/login" element={<Login></Login>}></Route>
          <Route path="/logout" element={<Logout></Logout>}></Route>
          <Route path="/signup" element={<RegisterAndLogout />}></Route>
          <Route path="/watchlist" element={<Watchlist></Watchlist>}></Route>
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Home></Home>
              </ProtectedRoute>
            }
          ></Route>
          <Route path="*" element={<NotFound></NotFound>}></Route>
        </Routes>
      </Router>
    </>
  );
}

export default App;
