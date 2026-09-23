import React, { useEffect, useState } from 'react';
import { Activity, AlertTriangle, CheckCircle, Clock, Truck } from 'lucide-react';
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

const Dashboard = () => {
  const [operator, setOperator] = useState(null);
  const [machine, setMachine] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [telemetry, setTelemetry] = useState([]);
  const [loading, setLoading] = useState(true);

  // For the prototype demo scenario
  const operatorId = 'OP1001';
  const machineId = 'EXC001';

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [opRes, machRes, tasksRes, telRes] = await Promise.all([
          api.get(`/operators/${operatorId}`),
          api.get(`/machines/${machineId}`),
          api.get('/tasks'),
          api.get(`/telemetry/${machineId}`)
        ]);
        
        setOperator(opRes.data);
        setMachine(machRes.data);
        setTasks(tasksRes.data.filter(t => t.operator_id === operatorId));
        setTelemetry(telRes.data);
      } catch (err) {
        console.error("Error fetching data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className="p-8 text-center text-gray-500">Loading Dashboard...</div>;
  if (!operator) return <div className="p-8 text-center text-red-500">Failed to load data. Ensure backend is running and seeded.</div>;

  const todayTask = tasks.find(t => t.status === 'In Progress') || tasks[0];

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-8 font-sans">
      <header className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-teal-400">
            Smart Operator Assistant
          </h1>
          <p className="text-slate-400 mt-1">CAT Machinery Intelligence Dashboard</p>
        </div>
        <div className="text-right">
          <div className="text-sm text-slate-400">Operator</div>
          <div className="font-semibold text-lg">{operator.name} ({operator.operator_id})</div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700 shadow-lg">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-slate-400 font-medium">Safety Score</h3>
            <CheckCircle className="text-emerald-400" size={20} />
          </div>
          <div className="text-4xl font-bold text-emerald-400">{operator.safety_score}%</div>
          <p className="text-sm text-slate-500 mt-2">Top 5% of operators</p>
        </div>

        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700 shadow-lg">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-slate-400 font-medium">Efficiency</h3>
            <Activity className="text-blue-400" size={20} />
          </div>
          <div className="text-4xl font-bold text-blue-400">{operator.efficiency_score}%</div>
          <p className="text-sm text-slate-500 mt-2">Optimal range</p>
        </div>

        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700 shadow-lg">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-slate-400 font-medium">Machine Status</h3>
            <Truck className="text-amber-400" size={20} />
          </div>
          <div className="text-2xl font-bold text-amber-400">{machine.machine_type} ({machine.machine_id})</div>
          <p className="text-sm text-slate-500 mt-2">{machine.engine_hours} hrs • {machine.status}</p>
        </div>
        
        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700 shadow-lg">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-slate-400 font-medium">Active Task</h3>
            <Clock className="text-purple-400" size={20} />
          </div>
          <div className="text-xl font-bold text-purple-400">{todayTask?.task_type}</div>
          <p className="text-sm text-slate-500 mt-2">Est: {todayTask?.estimated_time}m</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700 shadow-lg">
          <h3 className="text-xl font-semibold mb-6 text-slate-200">Recent Telemetry (Engine Hours)</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={telemetry.slice().reverse()}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="engine_hours" stroke="#94a3b8" />
                <YAxis yAxisId="left" stroke="#38bdf8" />
                <YAxis yAxisId="right" orientation="right" stroke="#f472b6" />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }} />
                <Legend />
                <Line yAxisId="left" type="monotone" dataKey="fuel_used" stroke="#38bdf8" name="Fuel Used (L)" strokeWidth={2} />
                <Line yAxisId="right" type="monotone" dataKey="idling_time" stroke="#f472b6" name="Idling (min)" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700 shadow-lg">
          <h3 className="text-xl font-semibold mb-6 text-slate-200">Task Performance History</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={tasks.filter(t => t.actual_time)}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="task_type" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }} />
                <Legend />
                <Bar dataKey="estimated_time" fill="#3b82f6" name="Estimated Time (m)" radius={[4, 4, 0, 0]} />
                <Bar dataKey="actual_time" fill="#10b981" name="Actual Time (m)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Safety & Intelligence Section (Placeholder for integration) */}
      <div className="bg-slate-800 rounded-xl p-6 border border-slate-700 shadow-lg">
        <h3 className="text-xl font-semibold mb-4 text-slate-200 flex items-center">
          <AlertTriangle className="mr-2 text-rose-500" />
          Live Safety & Intelligence Feed
        </h3>
        <div className="p-4 bg-slate-900 rounded-lg border border-slate-700 text-slate-400">
          Intelligence integration pending. Telemetry and prediction events will appear here.
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
