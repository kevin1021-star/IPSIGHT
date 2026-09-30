import { useState, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, Mail, Lock, AlertCircle, Loader2, Eye, EyeOff, PlayCircle } from 'lucide-react';
import { useAuth } from '../lib/auth';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState('analyst@praxis.iitj.ac.in');
  const [password, setPassword] = useState('SecOps@2026');
  const [showPass, setShowPass] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!email.trim() || !password.trim()) {
      setError('Email and password are required.');
      return;
    }
    setIsLoading(true);
    try {
      await login(email.trim(), password);
      navigate('/', { replace: true });
    } catch (err: unknown) {
      const msg =
        err instanceof Error
          ? err.message
          : 'Invalid credentials. Please try again.';
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoLogin = async () => {
    setIsLoading(true);
    try {
      await login('demo@praxis.iitj.ac.in', 'DemoSecOps2026!');
      navigate('/', { replace: true });
    } catch {
      navigate('/', { replace: true });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen auth-bg auth-grid flex items-center justify-center p-4 relative overflow-hidden bg-[#0a0f1e]">
      {/* Animated floating orbs */}
      <div className="absolute top-1/4 left-1/4 w-72 h-72 rounded-full bg-cyan-500/10 blur-3xl animate-pulse pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full bg-blue-600/10 blur-3xl animate-pulse pointer-events-none" style={{ animationDelay: '1.5s' }} />

      <div className="w-full max-w-md relative z-10">
        {/* Card */}
        <div className="bg-slate-900/90 border border-slate-700/60 rounded-2xl p-8 shadow-2xl backdrop-blur-md">
          {/* Logo */}
          <div className="flex flex-col items-center mb-6">
            <div className="relative mb-3">
              <div className="w-16 h-16 rounded-2xl bg-cyan-500/20 border border-cyan-400/40 flex items-center justify-center shadow-lg shadow-cyan-500/10">
                <Shield size={34} className="text-cyan-400" />
              </div>
              <div className="absolute inset-0 rounded-2xl bg-cyan-400/20 blur-xl" />
            </div>
            <h1 className="text-2xl font-black tracking-wider text-slate-100 uppercase">
              IP<span className="text-cyan-400">SIGHT</span>
            </h1>
            <p className="text-xs text-slate-400 mt-1 font-medium tracking-wide text-center">
              AI-Powered IPsec Protocol Analyzer & SecOps Platform
            </p>
            <span className="mt-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-cyan-950/80 border border-cyan-500/40 text-cyan-300">
              Team Praxis · IIT Jodhpur
            </span>
          </div>

          {/* Quick 1-Click Demo Button */}
          <button
            type="button"
            onClick={handleDemoLogin}
            disabled={isLoading}
            className="w-full mb-5 py-3 px-4 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold text-sm flex items-center justify-center gap-2 shadow-lg shadow-cyan-500/20 transition-all transform active:scale-98"
          >
            <PlayCircle size={18} />
            <span>⚡ Launch Live Demo / SecOps Preview</span>
          </button>

          <div className="relative flex py-2 items-center mb-4">
            <div className="flex-grow border-t border-slate-700/60"></div>
            <span className="flex-shrink mx-3 text-xs text-slate-500 uppercase tracking-wider font-semibold">Or Sign In with Credentials</span>
            <div className="flex-grow border-t border-slate-700/60"></div>
          </div>

          {/* Error alert */}
          {error && (
            <div className="mb-4 flex items-start gap-2.5 px-4 py-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
              <AlertCircle size={16} className="flex-shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email */}
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                SecOps Email Address
              </label>
              <div className="relative">
                <Mail size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none" />
                <input
                  type="email"
                  autoComplete="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="analyst@praxis.iitj.ac.in"
                  className="w-full bg-slate-950/80 border border-slate-700 rounded-lg pl-10 pr-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition-colors"
                  disabled={isLoading}
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                Password
              </label>
              <div className="relative">
                <Lock size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none" />
                <input
                  type={showPass ? 'text' : 'password'}
                  autoComplete="current-password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••"
                  className="w-full bg-slate-950/80 border border-slate-700 rounded-lg pl-10 pr-10 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition-colors"
                  disabled={isLoading}
                />
                <button
                  type="button"
                  onClick={() => setShowPass((v) => !v)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 transition-colors"
                  tabIndex={-1}
                >
                  {showPass ? <EyeOff size={15} /> : <Eye size={15} />}
                </button>
              </div>
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-2.5 px-4 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-600 text-slate-200 font-semibold text-sm flex items-center justify-center gap-2 transition-colors"
            >
              {isLoading ? (
                <>
                  <Loader2 size={16} className="animate-spin" />
                  <span>Authenticating…</span>
                </>
              ) : (
                <>
                  <Shield size={16} />
                  <span>Sign In</span>
                </>
              )}
            </button>
          </form>

          {/* Footer */}
          <p className="text-center text-xs text-slate-500 mt-5">
            100% Air-Gapped & Offline Ready · SIH 2026 (PS: SIH26160)
          </p>
        </div>

        {/* Version tag */}
        <p className="text-center text-xs text-slate-500 mt-4 font-mono">
          IPsight v2.0.0 · Team Praxis · Indian Institute of Technology Jodhpur
        </p>
      </div>
    </div>
  );
}
