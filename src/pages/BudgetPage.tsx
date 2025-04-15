import React, { useState, useEffect } from 'react';
import { PlusCircle, Trash2 } from 'lucide-react';
import { getTransactions, addTransaction, deleteTransaction } from '../api';
import { useTheme } from "../ThemeContext";
import { motion, AnimatePresence } from "framer-motion";


interface Expense {
  id: number;
  description: string;
  amount: number;
  category: string;
  date: string;
}

export default function BudgetPage() {

  const { darkMode } = useTheme();

  const [showInsightForm, setShowInsightForm] = useState(false);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');


  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [newExpense, setNewExpense] = useState({
    description: '',
    amount: '',
    category: 'Housing',
    date: new Date().toISOString().split('T')[0]
  });

  const categories = ['Housing', 'Food', 'Transportation', 'Entertainment', 'Healthcare', 'Shopping', 'Others'];

  // Fetch transactions from the database when the page loads
  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      const data = await getTransactions();
      setExpenses(data);
    } catch (error) {
      console.error('Error fetching transactions:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const expense = {
        description: newExpense.description,
        amount: parseFloat(newExpense.amount) || 0, // Ensure amount is a number
        category: newExpense.category,
        date: newExpense.date
      };

      await addTransaction(expense.description, expense.amount, expense.category, expense.date);

      // ✅ Update state immediately so UI refreshes
      await fetchTransactions();

      setShowForm(false);
      setNewExpense({
        description: '',
        amount: '',
        category: 'Housing',
        date: new Date().toISOString().split('T')[0]
      });
    } catch (error) {
      console.error('Error adding transaction:', error);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      console.log(`Attempting to delete transaction with ID: ${id}`);
      await deleteTransaction(id);
      console.log(`Transaction ${id} deleted successfully`);
      setExpenses(expenses.filter(expense => expense.id !== id)); // Remove from UI
    } catch (error) {
      console.error('Error deleting transaction:', error);
    }
  };
  
  const [showInsight, setShowInsight] = useState(false);
  const [insight, setInsight] = useState("");


  const fetchInsights = async () => {
    try {
      const response = await fetch("http://localhost:5000/insights", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          start_date: startDate,
          end_date: endDate,
        }),
      });

      const data = await response.json();
      setInsight(data.insight);
      setShowInsight(true);
    } catch (error) {
      console.error("Error fetching insight:", error);
      setInsight("Something went wrong fetching AI insights.");
      setShowInsight(true);
    }
  };
  


  return (
    <div className={`min-h-screen bg-gray-50 dark:bg-gray-900 py-8`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-xl shadow-lg p-8">

          {/* <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Budget Dashboard</h1>
            <button
              onClick={() => setShowForm(true)}
              className="flex items-center px-6 py-3 bg-orange-500 text-white rounded-full hover:bg-orange-600 transition-colors"
            >
              <PlusCircle className="h-5 w-5 mr-2" />
              Add Expense
            </button>
          </div> */}

          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Budget Dashboard</h1>
            <div className="flex space-x-4">
              <button
                onClick={() => setShowForm(true)}
                className="flex items-center px-6 py-3 bg-orange-500 text-white rounded-full hover:bg-orange-600 transition-colors"
              >
                <PlusCircle className="h-5 w-5 mr-2" />
                Add Expense
              </button>

              <button
                onClick={() => setShowInsightForm(true)}
                className="flex items-center px-6 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors shadow-glow-blue animate-pulse-glow"
              >
                💡 Get AI Insights
              </button>

              {/* Modal for Get AI Insights */}
              {showInsightForm && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
                  <div className="bg-white rounded-xl p-8 w-full max-w-md">
                    <h2 className="text-2xl font-bold mb-6">Get AI Insights</h2>
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
                        <input
                          type="date"
                          value={startDate}
                          onChange={(e) => setStartDate(e.target.value)}
                          className="w-full rounded-lg border-gray-300 shadow-sm focus:border-orange-500 focus:ring-orange-500"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
                        <input
                          type="date"
                          value={endDate}
                          onChange={(e) => setEndDate(e.target.value)}
                          className="w-full rounded-lg border-gray-300 shadow-sm focus:border-orange-500 focus:ring-orange-500"
                        />
                      </div>
                    </div>
                    <div className="mt-6 flex justify-end space-x-3">
                      <button
                        type="button"
                        onClick={() => setShowInsightForm(false)}
                        className="px-4 py-2 text-gray-700"
                      >
                        Cancel
                      </button>
                      <button
                        onClick={fetchInsights}
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                      >
                        Submit & Get Insights
                      </button>
                    </div>
                  </div>
                </div>
              )}
              </div>
            </div>

            {showForm && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
              <div className="bg-white rounded-xl p-8 w-full max-w-md">
                <h2 className="text-2xl font-bold mb-6">Add New Expense</h2>
                <form onSubmit={handleSubmit}>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                      <input
                        type="text"
                        required
                        value={newExpense.description}
                        onChange={(e) => setNewExpense({ ...newExpense, description: e.target.value })}
                        className="w-full rounded-lg border-gray-300 shadow-sm focus:border-orange-500 focus:ring-orange-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Amount (₹)</label>
                      <input
                        type="text"
                        required
                        min="0"
                        step="0.01"
                        value={newExpense.amount}
                        onChange={(e) => {
                          const value = e.target.value;
                          if (/^\d*\.?\d*$/.test(value)) {  // ✅ Prevents leading zeros & allows only valid numbers
                            setNewExpense({ ...newExpense, amount: value });
                          }
                        }}
                        className="w-full rounded-lg border-gray-300 shadow-sm focus:border-orange-500 focus:ring-orange-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                      <select
                        value={newExpense.category}
                        onChange={(e) => setNewExpense({ ...newExpense, category: e.target.value })}
                        className="w-full rounded-lg border-gray-300 shadow-sm focus:border-orange-500 focus:ring-orange-500"
                      >
                        {categories.map((category) => (
                          <option key={category} value={category}>
                            {category}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
                      <input
                        type="date"
                        required
                        value={newExpense.date}
                        onChange={(e) => setNewExpense({ ...newExpense, date: e.target.value })}
                        className="w-full rounded-lg border-gray-300 shadow-sm focus:border-orange-500 focus:ring-orange-500"
                      />
                    </div>
                  </div>
                  <div className="mt-6 flex justify-end space-x-3">
                    <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 text-gray-700">
                      Cancel
                    </button>
                    <button type="submit" className="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600">
                      Add Expense
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}

          
          <AnimatePresence>
          {showInsight && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.4, ease: "easeInOut" }}
              className="overflow-hidden mt-8 bg-blue-50 border border-blue-200 text-blue-800 rounded-lg p-6 shadow"
            >
              <div className="flex justify-between items-center mb-2">
                <h2 className="text-xl font-semibold">💬 AI Insights</h2>
                <button
                  onClick={() => setShowInsight(false)}
                  className="text-sm text-blue-700 hover:text-blue-900"
                >
                  Close ✖
                </button>
              </div>
              <p className="whitespace-pre-line">{insight}</p>
            </motion.div>
          )}
        </AnimatePresence>

          {/* Transaction List */}
          <div className="mt-6">
            <h2 className="text-2xl font-semibold mb-4">Transaction History</h2>
            {expenses.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full border border-gray-200">
                  <thead className="bg-gray-100">
                    <tr>
                      <th className="px-4 py-2 border">Date</th>
                      <th className="px-4 py-2 border">Description</th>
                      <th className="px-4 py-2 border">Category</th>
                      <th className="px-4 py-2 border">Amount</th>
                      <th className="px-4 py-2 border text-center">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {expenses.map((expense) => (
                      <tr key={expense.id} className="border">
                        <td className="px-4 py-2 border">{expense.date}</td>
                        <td className="px-4 py-2 border">{expense.description}</td>
                        <td className="px-4 py-2 border">{expense.category}</td>
                        <td className="px-4 py-2 border">₹{expense.amount.toFixed(2)}</td>
                        <td className="px-4 py-2 border text-center">
                          <button 
                            onClick={() => handleDelete(expense.id)}
                            className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-700 transition flex items-center"
                          >
                            <Trash2 className="h-4 w-4 mr-1" />
                            Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-gray-500">No expenses added yet.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
