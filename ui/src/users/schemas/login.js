
export default {
  layout: {
    rows: [
      {
        fields: [
          {
            type: 'text',
            name: 'loginDetail.loginName',
            'md-type': true,
            placeholder: 'Login Name',
            validations: {
              required: {
                message: 'Login Name is mandatory'
              }
            }
          }
        ]
      },
      {
        fields: [
          {
            type: 'password',
            name: 'loginDetail.password',
            'md-type': true,
            placeholder: 'Password',
            validations: {
              required: {
                message: 'Password is mandatory'
              }
            }
          }
        ]
      },
      {
        fields: [
          {
            type: 'text',
            name: 'loginDetail.props.otp',
            'md-type': true,
            placeholder: 'OTP',
            validations: {
              required: {
                message: 'OTP is mandatory'
              }
            },
            showWhen: 'otpAuthEnabled'
          }
        ]
      },
    ]
  }
}
