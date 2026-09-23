import React, { useEffect, useState } from 'react';
import {
  ShieldCheck,
  Zap,
  Truck,
  Clock,
  AlertTriangle,
  Play,
  RotateCcw,
  Sparkles,
  CheckCircle2,
  Sliders,
  TrendingUp,
  Cpu,
  GraduationCap
} from 'lucide-react';
import api from '../services/api';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  Legend
} from 'recharts';

const OPERATORS_LIST = [
  { id: 'OP1001', name: 'John Doe', skill: 'Expert' },
  { id: 'OP1002', name: 'Jane Smith', skill: 'Intermediate' },
  { id: 'OP1003', name: 'Bob Johnson', skill: 'Beginner' }
];

const MACHINES_LIST = [
  { id: 'EXC001', name: 'CAT 320 Hydraulic Excavator' },
  { id: 'DOZ002', name: 'CAT D6 Track-Type Dozer' },
  { id: 'TRK003', name: 'CAT 777 Haul Truck' }
];

const Dashboard = () => {
  // Selection states
  const [selectedOpId, setSelectedOpId] = useState('OP1001');
  const [selectedMachId, setSelectedMachId] = useState('EXC001');

  // Loaded data
  const [operator, setOperator] = useState(null);
  const [machine, setMachine] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [telemetry, setTelemetry] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  // Telemetry Simulator inputs
  const [simFuel, setSimFuel] = useState(18.5);
  const [simIdling, setSimIdling] = useState(5.0);
  const [simSeatbelt, setSimSeatbelt] = useState('Fastened');
  const [simSafetyAlert, setSimSafetyAlert] = useState(false);
  const [simSending, setSimSending] = useState(false);
  const [lastSimResult, setLastSimResult] = useState(null);

  // ML Predictor inputs
  const [predTaskType, setPredTaskType] = useState('Earth Excavation');
  const [predWeather, setPredWeather] = useState('Rainy');
  const [predMachineAge, setPredMachineAge] = useState(3);
  const [predBaseTime, setPredBaseTime] = useState(60);
  const [predicting, setPredicting] = useState(false);
  const [predResult, setPredResult] = useState(null);

  // Enrolled courses state
  const [enrolledCourses, setEnrolledCourses] = useState({});

  // Fetch full data for selected operator & machine
  const fetchDashboardData = async (opId, machId) => {
    try {
      setLoading(true);
      const [opRes, machRes, tasksRes, telRes, recRes] = await Promise.all([
        api.get(`/operators/${opId}`),
        api.get(`/machines/${machId}`),
        api.get('/tasks/'),
        api.get(`/telemetry/${machId}`),
        api.get(`/analytics/operator/${opId}`).then(() => api.get(`/training/recommendations/${opId}`)).catch(() => ({ data: [] }))
      ]);

      setOperator(opRes.data);
      setMachine(machRes.data);
      setTasks(tasksRes.data.filter(t => t.operator_id === opId));
      setTelemetry(telRes.data);
      setRecommendations(recRes.data || []);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData(selectedOpId, selectedMachId);
  }, [selectedOpId, selectedMachId]);

  // Handle Preset Simulation Clicks
  const applyPreset = (preset) => {
    if (preset === 'normal') {
      setSimFuel(16.0);
      setSimIdling(4.0);
      setSimSeatbelt('Fastened');
      setSimSafetyAlert(false);
    } else if (preset === 'idle_waste') {
      setSimFuel(32.5);
      setSimIdling(45.0);
      setSimSeatbelt('Fastened');
      setSimSafetyAlert(false);
    } else if (preset === 'danger') {
      setSimFuel(42.0);
      setSimIdling(35.0);
      setSimSeatbelt('Unfastened');
      setSimSafetyAlert(true);
    }
  };

  // Submit Simulated Telemetry to Backend ML Engine
  const transmitTelemetry = async () => {
    setSimSending(true);
    try {
      const payload = {
        machine_id: selectedMachId,
        operator_id: selectedOpId,
        engine_hours: Number((machine?.engine_hours || 1500) + 1.2),
        fuel_used: Number(simFuel),
        load_cycles: 8,
        idling_time: Number(simIdling),
        seatbelt_status: simSeatbelt,
        safety_alert: simSafetyAlert
      };

      const res = await api.post('/telemetry/', payload);
      setLastSimResult(res.data);

      // Refresh telemetry and recommendations to reflect new machine state
      const [newTel, newRec, newOp] = await Promise.all([
        api.get(`/telemetry/${selectedMachId}`),
        api.get(`/training/recommendations/${selectedOpId}`).catch(() => ({ data: [] })),
        api.get(`/operators/${selectedOpId}`)
      ]);
      setTelemetry(newTel.data);
      setRecommendations(newRec.data || []);
      setOperator(newOp.data);
    } catch (err) {
      console.error('Error sending telemetry:', err);
    } finally {
      setSimSending(false);
    }
  };

  // Run ML Task Time Prediction
  const runMLPrediction = async () => {
    setPredicting(true);
    try {
      const res = await api.post('/predict/task-time', {
        task_type: predTaskType,
        weather: predWeather,
        operator_skill: operator?.skill_level || 'Intermediate',
        machine_age: Number(predMachineAge),
        estimated_time: Number(predBaseTime)
      });
      setPredResult(res.data);
    } catch (err) {
      console.error('Prediction failed:', err);
    } finally {
      setPredicting(false);
    }
  };

  const toggleEnroll = (index) => {
    setEnrolledCourses(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  if (loading && !operator) {
    return (
      <div className="app-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <div style={{ textAlign: 'center' }}>
          <div className="cat-badge" style={{ display: 'inline-block', marginBottom: '16px' }}>CAT INTELLIGENCE</div>
          <h2 style={{ fontSize: '1.5rem', color: '#FFCD11' }}>Connecting to Machine Telemetry Gateway...</h2>
          <p style={{ color: '#94A3B8', marginTop: '8px' }}>Initializing PostgreSQL and AI Neural Models</p>
        </div>
      </div>
    );
  }

  const activeTask = tasks.find(t => t.status === 'In Progress') || tasks[0];

  return (
    <div className="app-container">
      {/* Top Header */}
      <header className="header-bar">
        <div className="brand-section">
          <div className="cat-badge">CAT</div>
          <div>
            <h1 className="brand-title">Smart Operator Assistant</h1>
            <div className="brand-sub">
              <span className="status-dot"></span>
              <span>TELEMETRY GATEWAY: ONLINE</span>
              <span>•</span>
              <span style={{ color: '#FFCD11' }}>PORT 8001 LINKED</span>
            </div>
          </div>
        </div>

        <div className="controls-cluster">
          {/* Operator Switcher */}
          <div className="selector-pill">
            <span style={{ color: '#94A3B8' }}>Operator:</span>
            <select
              value={selectedOpId}
              onChange={(e) => setSelectedOpId(e.target.value)}
            >
              {OPERATORS_LIST.map(op => (
                <option key={op.id} value={op.id}>{op.name} ({op.skill})</option>
              ))}
            </select>
          </div>

          {/* Machine Switcher */}
          <div className="selector-pill">
            <span style={{ color: '#94A3B8' }}>Machinery:</span>
            <select
              value={selectedMachId}
              onChange={(e) => setSelectedMachId(e.target.value)}
            >
              {MACHINES_LIST.map(m => (
                <option key={m.id} value={m.id}>{m.id} - {m.name}</option>
              ))}
            </select>
          </div>

          <button
            className="preset-chip"
            style={{ display: 'flex', alignItems: 'center', gap: '6px' }}
            onClick={() => fetchDashboardData(selectedOpId, selectedMachId)}
          >
            <RotateCcw size={14} /> Refresh Stream
          </button>
        </div>
      </header>

      {/* KPI Stat Cards Cluster */}
      <div className="kpi-grid">
        {/* Safety Score */}
        <div className="kpi-card safety">
          <div className="kpi-top">
            <span className="kpi-label">Safety Compliance</span>
            <div className="kpi-icon" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#10B981' }}>
              <ShieldCheck size={20} />
            </div>
          </div>
          <div className="kpi-val" style={{ color: operator?.safety_score >= 80 ? '#10B981' : '#EF4444' }}>
            {operator?.safety_score || 0}<span className="kpi-unit">%</span>
          </div>
          <div className="kpi-sub">
            <span style={{ color: operator?.safety_score >= 80 ? '#10B981' : '#EF4444', fontWeight: 600 }}>
              {operator?.safety_score >= 85 ? 'Fleet Safe Tier 1' : 'Action Required'}
            </span>
            <span>• {operator?.skill_level} Operator</span>
          </div>
        </div>

        {/* Operational Efficiency */}
        <div className="kpi-card efficiency">
          <div className="kpi-top">
            <span className="kpi-label">Efficiency Index</span>
            <div className="kpi-icon" style={{ background: 'rgba(56, 189, 248, 0.15)', color: '#38BDF8' }}>
              <Zap size={20} />
            </div>
          </div>
          <div className="kpi-val" style={{ color: '#38BDF8' }}>
            {operator?.efficiency_score || 0}<span className="kpi-unit">%</span>
          </div>
          <div className="kpi-sub">
            <TrendingUp size={14} style={{ color: '#10B981' }} />
            <span>Optimal hydraulic cycle matching</span>
          </div>
        </div>

        {/* Machine Status */}
        <div className="kpi-card machine">
          <div className="kpi-top">
            <span className="kpi-label">Active Machinery</span>
            <div className="kpi-icon" style={{ background: 'rgba(255, 205, 17, 0.15)', color: '#FFCD11' }}>
              <Truck size={20} />
            </div>
          </div>
          <div className="kpi-val" style={{ color: '#FFCD11', fontSize: '1.9rem' }}>
            {machine?.machine_id}
          </div>
          <div className="kpi-sub">
            <span>{machine?.engine_hours || 0} hrs</span>
            <span>•</span>
            <span style={{ color: '#10B981', fontWeight: 600 }}>{machine?.status?.toUpperCase()}</span>
          </div>
        </div>

        {/* Active Work Order */}
        <div className="kpi-card task">
          <div className="kpi-top">
            <span className="kpi-label">Assigned Work Order</span>
            <div className="kpi-icon" style={{ background: 'rgba(168, 85, 247, 0.15)', color: '#A855F7' }}>
              <Clock size={20} />
            </div>
          </div>
          <div className="kpi-val" style={{ color: '#C084FC', fontSize: '1.6rem' }}>
            {activeTask ? activeTask.task_type : 'Ready For Dispatch'}
          </div>
          <div className="kpi-sub">
            <span>Target: {activeTask?.estimated_time || 45} mins</span>
            <span>•</span>
            <span>Weather: {activeTask?.weather || 'Clear'}</span>
          </div>
        </div>
      </div>

      {/* Main 2-Column Grid: Live Simulator & AI Predictor */}
      <div className="content-grid-2col">
        {/* Panel 1: Live Telemetry & Incident Simulator */}
        <div className="dashboard-panel">
          <div className="panel-header">
            <div className="panel-title">
              <Sliders size={20} style={{ color: '#FFCD11' }} />
              Live Telemetry & Anomaly Trigger
            </div>
            <span className="panel-tag" style={{ background: 'rgba(255, 205, 17, 0.15)', color: '#FFCD11' }}>
              Real-Time Feed
            </span>
          </div>

          {/* Quick Preset Buttons */}
          <div className="preset-bar">
            <span style={{ fontSize: '0.8rem', color: '#94A3B8', alignSelf: 'center' }}>Demo Scenarios:</span>
            <button className="preset-chip" onClick={() => applyPreset('normal')}>🟢 Normal Digging</button>
            <button className="preset-chip" onClick={() => applyPreset('idle_waste')}>🟡 High Idle Waste</button>
            <button className="preset-chip" onClick={() => applyPreset('danger')}>🔴 Seatbelt Violation</button>
          </div>

          <div className="sim-controls-grid">
            <div className="control-field">
              <label>
                <span>Fuel Burn Rate</span>
                <span style={{ color: '#FFCD11' }}>{simFuel} L/hr</span>
              </label>
              <input
                type="range"
                min="5"
                max="60"
                step="0.5"
                value={simFuel}
                onChange={(e) => setSimFuel(parseFloat(e.target.value))}
              />
            </div>

            <div className="control-field">
              <label>
                <span>Idling Duration</span>
                <span style={{ color: simIdling > 30 ? '#EF4444' : '#38BDF8' }}>{simIdling} min</span>
              </label>
              <input
                type="range"
                min="0"
                max="60"
                step="1"
                value={simIdling}
                onChange={(e) => setSimIdling(parseFloat(e.target.value))}
              />
            </div>

            <div className="control-field">
              <label>
                <span>Seatbelt Status</span>
                <span style={{ color: simSeatbelt === 'Fastened' ? '#10B981' : '#EF4444' }}>{simSeatbelt}</span>
              </label>
              <div className="toggle-group">
                <button
                  className={`toggle-btn ${simSeatbelt === 'Fastened' ? 'active safe' : ''}`}
                  onClick={() => setSimSeatbelt('Fastened')}
                >
                  Fastened
                </button>
                <button
                  className={`toggle-btn ${simSeatbelt === 'Unfastened' ? 'active danger' : ''}`}
                  onClick={() => setSimSeatbelt('Unfastened')}
                >
                  Unfastened
                </button>
              </div>
            </div>

            <div className="control-field">
              <label>
                <span>Cabin Safety Sensor</span>
                <span style={{ color: simSafetyAlert ? '#EF4444' : '#10B981' }}>{simSafetyAlert ? 'TRIGGERED' : 'CLEAR'}</span>
              </label>
              <div className="toggle-group">
                <button
                  className={`toggle-btn ${!simSafetyAlert ? 'active safe' : ''}`}
                  onClick={() => setSimSafetyAlert(false)}
                >
                  Normal
                </button>
                <button
                  className={`toggle-btn ${simSafetyAlert ? 'active danger' : ''}`}
                  onClick={() => setSimSafetyAlert(true)}
                >
                  Alarm ON
                </button>
              </div>
            </div>
          </div>

          <button
            className="action-btn-primary"
            onClick={transmitTelemetry}
            disabled={simSending}
          >
            <Play size={18} />
            {simSending ? 'Transmitting to ML Engine...' : 'Transmit Telemetry Event'}
          </button>

          {/* Incident / Success Feedback Banner */}
          {lastSimResult && (
            <div className={`incident-alert-banner ${lastSimResult.safety_analysis?.risk_level === 'SAFE' ? 'safe-banner' : ''}`}>
              {lastSimResult.safety_analysis?.risk_level !== 'SAFE' ? (
                <>
                  <AlertTriangle size={24} style={{ color: '#EF4444', flexShrink: 0, marginTop: '2px' }} />
                  <div>
                    <div style={{ color: '#EF4444', fontWeight: 700, fontSize: '0.95rem' }}>
                      SAFETY ALERT: {lastSimResult.safety_analysis?.risk_level} (Score: {lastSimResult.safety_analysis?.safety_score}%)
                    </div>
                    <div style={{ color: '#FCA5A5', fontSize: '0.85rem', marginTop: '4px' }}>
                      Violations: {lastSimResult.safety_analysis?.reasons?.join(', ') || 'Abnormal operations flagged'}
                    </div>
                    <div style={{ color: '#94A3B8', fontSize: '0.78rem', marginTop: '4px' }}>
                      Action: Safety incident logged. Auto-assigned corrective training modules below.
                    </div>
                  </div>
                </>
              ) : (
                <>
                  <CheckCircle2 size={24} style={{ color: '#10B981', flexShrink: 0, marginTop: '2px' }} />
                  <div>
                    <div style={{ color: '#10B981', fontWeight: 700, fontSize: '0.95rem' }}>
                      SAFE TELEMETRY RECEIVED
                    </div>
                    <div style={{ color: '#A7F3D0', fontSize: '0.85rem', marginTop: '4px' }}>
                      ML Isolation Forest evaluated operating conditions within normal parameters.
                    </div>
                  </div>
                </>
              )}
            </div>
          )}
        </div>

        {/* Panel 2: Real-Time ML Task Predictor */}
        <div className="dashboard-panel">
          <div className="panel-header">
            <div className="panel-title">
              <Cpu size={20} style={{ color: '#38BDF8' }} />
              ML Task Completion Time Predictor
            </div>
            <span className="panel-tag" style={{ background: 'rgba(56, 189, 248, 0.15)', color: '#38BDF8' }}>
              RandomForest AI
            </span>
          </div>

          <div className="predictor-form-grid">
            <div className="predictor-field">
              <label>Work Order Type</label>
              <select value={predTaskType} onChange={(e) => setPredTaskType(e.target.value)}>
                <option value="Earth Excavation">Earth Excavation</option>
                <option value="Trenching">Trenching</option>
                <option value="Loading">Loading & Hauling</option>
                <option value="Site Grading">Site Grading</option>
              </select>
            </div>

            <div className="predictor-field">
              <label>Weather Condition</label>
              <select value={predWeather} onChange={(e) => setPredWeather(e.target.value)}>
                <option value="Clear">Clear Sky / Dry</option>
                <option value="Rainy">Heavy Rain</option>
                <option value="Muddy">Deep Mud / Sludge</option>
                <option value="Stormy">Severe Storm</option>
              </select>
            </div>

            <div className="predictor-field">
              <label>Base Planned Time (Mins)</label>
              <input
                type="number"
                min="10"
                max="240"
                value={predBaseTime}
                onChange={(e) => setPredBaseTime(e.target.value)}
              />
            </div>

            <div className="predictor-field">
              <label>Machine Age (Years)</label>
              <input
                type="number"
                min="0"
                max="15"
                value={predMachineAge}
                onChange={(e) => setPredMachineAge(e.target.value)}
              />
            </div>
          </div>

          <button
            className="action-btn-primary"
            style={{ background: 'linear-gradient(135deg, #38BDF8 0%, #0284C7 100%)', color: '#fff', boxShadow: '0 4px 14px rgba(56, 189, 248, 0.3)' }}
            onClick={runMLPrediction}
            disabled={predicting}
          >
            <Sparkles size={18} />
            {predicting ? 'Calculating ML Inference...' : 'Calculate AI Completion Estimate'}
          </button>

          {/* Prediction Result Display */}
          {predResult && (
            <div className="prediction-result-card">
              <div className="result-row">
                <span style={{ fontSize: '0.85rem', color: '#94A3B8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  Predicted Time
                </span>
                <span style={{ fontSize: '0.8rem', background: 'rgba(255, 205, 17, 0.15)', color: '#FFCD11', padding: '2px 8px', borderRadius: '4px', fontWeight: 600 }}>
                  Confidence: {predResult.confidence}%
                </span>
              </div>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '12px' }}>
                <div className="result-big-val">{predResult.predicted_time} <span style={{ fontSize: '1.1rem', color: '#94A3B8' }}>mins</span></div>
                <div style={{ fontSize: '0.9rem', color: predResult.predicted_time > predBaseTime ? '#F59E0B' : '#10B981', fontWeight: 600 }}>
                  {predResult.predicted_time > predBaseTime ? `+${(predResult.predicted_time - predBaseTime).toFixed(1)}m delay risk` : 'Optimal pace'}
                </div>
              </div>
              <div style={{ fontSize: '0.8rem', color: '#64748B', marginTop: '6px' }}>
                Engineered based on {operator?.name}'s {operator?.skill_level} rating & {predWeather} ground conditions.
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Row: Analytics Charts (Fuel & Idling + Task Performance) */}
      <div className="content-grid-2col">
        {/* Fuel & Idle Trends */}
        <div className="dashboard-panel">
          <div className="panel-header">
            <div className="panel-title">
              <TrendingUp size={20} style={{ color: '#38BDF8' }} />
              Telemetry Trend (Fuel vs Idling)
            </div>
            <span className="panel-tag" style={{ background: 'rgba(255,255,255,0.08)', color: '#94A3B8' }}>
              Historical Log
            </span>
          </div>
          <div className="chart-box">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={telemetry.slice().reverse()}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                <XAxis dataKey="engine_hours" stroke="#64748B" tick={{ fontSize: 12 }} />
                <YAxis yAxisId="left" stroke="#38BDF8" tick={{ fontSize: 12 }} />
                <YAxis yAxisId="right" orientation="right" stroke="#F43F5E" tick={{ fontSize: 12 }} />
                <Tooltip />
                <Legend wrapperStyle={{ paddingTop: '10px' }} />
                <Line yAxisId="left" type="monotone" dataKey="fuel_used" stroke="#38BDF8" name="Fuel Burn (L)" strokeWidth={3} dot={{ r: 3 }} />
                <Line yAxisId="right" type="monotone" dataKey="idling_time" stroke="#F43F5E" name="Idling (min)" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Task Performance History */}
        <div className="dashboard-panel">
          <div className="panel-header">
            <div className="panel-title">
              <Clock size={20} style={{ color: '#FFCD11' }} />
              Task Execution Performance (Est. vs Actual)
            </div>
            <span className="panel-tag" style={{ background: 'rgba(255, 205, 17, 0.15)', color: '#FFCD11' }}>
              Precision Analytics
            </span>
          </div>
          <div className="chart-box">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={tasks.filter(t => t.actual_time)}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                <XAxis dataKey="task_type" stroke="#64748B" tick={{ fontSize: 12 }} />
                <YAxis stroke="#64748B" tick={{ fontSize: 12 }} />
                <Tooltip />
                <Legend wrapperStyle={{ paddingTop: '10px' }} />
                <Bar dataKey="estimated_time" fill="#3B82F6" name="Planned (min)" radius={[4, 4, 0, 0]} />
                <Bar dataKey="actual_time" fill="#10B981" name="Actual (min)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* AI Safety & Training Recommendations Hub */}
      <div className="dashboard-panel" style={{ marginBottom: '28px' }}>
        <div className="panel-header">
          <div className="panel-title">
            <GraduationCap size={22} style={{ color: '#FFCD11' }} />
            Adaptive AI Safety Coaching & Training Recommendations
          </div>
          <span className="panel-tag" style={{ background: 'rgba(255, 205, 17, 0.15)', color: '#FFCD11' }}>
            Auto-Generated by Safety Engine
          </span>
        </div>

        {recommendations.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '32px', color: '#94A3B8' }}>
            <CheckCircle2 size={36} style={{ color: '#10B981', margin: '0 auto 12px' }} />
            <h4 style={{ color: '#fff', fontSize: '1.1rem' }}>No Urgent Corrective Training Required</h4>
            <p style={{ fontSize: '0.85rem', marginTop: '4px' }}>
              {operator?.name} has maintained compliant operating parameters. Trigger an incident simulation above to see live coaching assignment.
            </p>
          </div>
        ) : (
          <div className="rec-list">
            {recommendations.map((rec, index) => (
              <div key={index} className="rec-item">
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '4px' }}>
                    <span className={rec.priority === 'High' ? 'rec-badge-high' : 'rec-badge-med'}>
                      {rec.priority} Priority
                    </span>
                    <span style={{ fontSize: '0.8rem', color: '#94A3B8' }}>{rec.category}</span>
                    <span style={{ fontSize: '0.8rem', color: '#64748B' }}>• {rec.duration} mins</span>
                  </div>
                  <h4 style={{ color: '#fff', fontSize: '1rem', fontWeight: 600 }}>{rec.title}</h4>
                  <p style={{ color: '#94A3B8', fontSize: '0.84rem', marginTop: '2px' }}>{rec.reason}</p>
                </div>
                <button
                  className={`enroll-btn ${enrolledCourses[index] ? 'enrolled' : ''}`}
                  onClick={() => toggleEnroll(index)}
                >
                  {enrolledCourses[index] ? '✓ Enrolled in LMS' : 'Enroll Operator'}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="footer-bar">
        Caterpillar Inc. Smart Operator Assistant Prototype • Hackathon Ready Demo • FastAPI Backend on Port 8001
      </footer>
    </div>
  );
};

export default Dashboard;
