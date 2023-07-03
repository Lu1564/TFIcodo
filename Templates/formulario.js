const LoginForm = {
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    login() {
      axios
        .post('http://localhost:5000/login' , { email: this.email, password: this.password })
        .then(response => {
         
          console.log(response)
          window.location.href = 'http://localhost:5000/protected';

        })
        .catch(error => {
          
        });
    }
  },
  template: `
    <div>
      <h3>Cliente registrado</h3>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" class="form-control" v-model="email" required>
        </div>
        <div class="form-group">
          <label for="password">Contraseña:</label>
          <input type="password" class="form-control" v-model="password" required>
        </div>
        <button type="submit" class="btn btn-primary">Iniciar sesión</button>
      </form>
    </div>
  `
};

const SigninForm ={
  data() {
      return {
        email: '',
        password: ''
      };
    },
  methods: {
      signin() {
        axios
          .post('http://localhost:5000/signin' , { email: this.email, password: this.password })
          .then(response => {
           
            console.log(response)
            window.location.href = 'http://localhost:5000/inicio';
  
          })
          .catch(error => {
            
          });
      }
  },
  template: `
  <div>
    <h3>Registrar cliente</h3>
    <form @submit.prevent="signin">
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" class="form-control" v-model="email" required>
      </div>
      <div class="form-group">
        <label for="password">Contraseña:</label>
        <input type="password" class="form-control" v-model="password" required>
      </div>
      <button type="submit" class="btn btn-primary">Registrar</button>
    </form>
  </div>
`  
};
    


const app = Vue.createApp({
  components: {
    'login-form': LoginForm,
    'signin-form': SigninForm
  }
});

app.mount('#app');




