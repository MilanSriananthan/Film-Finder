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
import SignUpPage from "./pages/SignUpPage";
import ListWatch from "./pages/ListWatch";
import AllMovies from "./pages/AllMovies";
import SearchView from "./pages/SearchView";

function Logout() {
  localStorage.clear();
  return <Navigate to="/login"></Navigate>;
}

//function RegisterAndLogout() {
//localStorage.clear();
// return <Naviggate to="/signup"></Navigate>;
//}

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/login" element={<Login></Login>}></Route>
          <Route path="/logout" element={<Logout></Logout>}></Route>
          <Route path="/signup" element={<SignUpPage></SignUpPage>}></Route>
          <Route
            path="/watchlist"
            element={
              <ProtectedRoute>
                <ListWatch></ListWatch>
              </ProtectedRoute>
            }
          ></Route>
          <Route
            path="/search"
            element={
              <ProtectedRoute>
                <SearchView></SearchView>
              </ProtectedRoute>
            }
          ></Route>
          <Route
            path="/movies"
            element={
              <ProtectedRoute>
                <AllMovies></AllMovies>
              </ProtectedRoute>
            }
          ></Route>
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
