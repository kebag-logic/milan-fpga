import numpy as np
# state x = [I, u_prev, phi, phi_prev_window_mean_input(Theta_{n-1}), phi_nm1]
# per window n (512 ms):
#   e_n = E - u_{n-1}
#   phi_{n+1} = phi_n + e_n          (ns; DUT late = +)
#   Theta_n = (phi_n + phi_{n+1})/2  (window mean)
#   I_{n+1} = I_n + e_n/2 + g*Theta_{n-1}
#   u_n = I_{n+1} + e_n/4
def poles(g, kp=0.25, ki=0.5, delay=1):
    # state: I, u, phi, Th1 (Theta_{n-1})
    # e = -u (E=0)
    A = np.zeros((4,4))
    # phi' = phi - u
    # Theta_n = phi - u/2
    # I' = I - u*ki + g*Th1
    # u' = I' - kp*u = I - (ki+kp)u + g*Th1
    # Th1' = Theta_n = phi - u/2  (if delay=1) else uses current
    A[0] = [1, -ki, 0, g]
    A[1] = [1, -(ki+kp), 0, g]
    A[2] = [0, -1, 1, 0]
    A[3] = [0, -0.5, 1, 0]
    return np.linalg.eigvals(A)
for g in (0, 3/128, 6/128):
    p = poles(g)
    print(g, sorted(p, key=lambda z: -abs(z)), [abs(z) for z in p])
