// MongoDB schema and sample queries for Smart Home Service Assistant

// USERS
// {
//   _id: ObjectId,
//   name: String,
//   email: String, // unique
//   phone: String,
//   country: String,
//   state: String,
//   password: String, // hashed
//   role: "user" | "admin",
//   created_at: Date
// }

db.users.createIndex({ email: 1 }, { unique: true });

// TECHNICIANS
// {
//   _id: ObjectId,
//   name: String,
//   service_type: String,
//   experience: Number,
//   location: {
//     city: String,
//     lat: Number,
//     lng: Number
//   },
//   contact: String,
//   photo: String,
//   rating: Number,
//   approved: Boolean,
//   created_at: Date
// }

db.technicians.createIndex({ service_type: 1, approved: 1 });

// BOOKINGS
// {
//   _id: ObjectId,
//   user_id: String,
//   technician_id: String,
//   service_type: String,
//   issue_description: String,
//   scheduled_at: String,
//   status: "requested" | "confirmed" | "completed" | "cancelled",
//   created_at: Date
// }

db.bookings.createIndex({ user_id: 1, status: 1 });

// CHAT HISTORY
// {
//   _id: ObjectId,
//   user_id: String,
//   message: String,
//   classification: {
//     service_type: String,
//     confidence: Number,
//     reason: String
//   },
//   created_at: Date
// }

// Sample query: approved nearby plumbers (distance calculated in API)
db.technicians.find({ service_type: "plumber", approved: true });
