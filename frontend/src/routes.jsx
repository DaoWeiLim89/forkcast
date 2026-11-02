import { Navigate, Route, Routes } from "react-router-dom";
import SignInPage from "./features/auth/SignInPage";
import SignUpPage from "./features/auth/SignUpPage";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/sign-in" replace />} />
      <Route path="/sign-in" element={<SignInPage />} />
      <Route path="/sign-up" element={<SignUpPage />} />
      <Route path="*" element={<p>Page not found</p>} />
    </Routes>
  );
}