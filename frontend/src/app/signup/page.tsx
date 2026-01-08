import { AuthForm } from "@/components/auth/AuthForm";

export const metadata = {
  title: "Sign Up - Todo App",
  description: "Create your Todo App account",
};

export default function SignupPage() {
  return <AuthForm mode="signup" />;
}
