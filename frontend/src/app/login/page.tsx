import { AuthForm } from "@/components/auth/AuthForm";

export const metadata = {
  title: "Sign In - Todo App",
  description: "Sign in to your Todo App account",
};

export default function LoginPage() {
  return <AuthForm mode="login" />;
}
