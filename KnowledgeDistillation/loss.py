import torch
from torch.nn import functional as F


class DistillationLoss(torch.nn.Module):
    def __init__(self, base_criterion, teacher_model, distillation_type, alpha, tau):
        super().__init__()
        self.base_criterion = base_criterion
        self.teacher_model = teacher_model
        self.distillation_type = distillation_type
        self.alpha = alpha
        self.tau = tau

    def forward(self, inputs, outputs, labels):
        outputs_kd = None
        if not isinstance(outputs, torch.Tensor):
            outputs, outputs_kd = outputs

        base_loss = self.base_criterion(outputs, labels)

        if self.distillation_type == 'none':
            return base_loss
        
        with torch.no_grad():
            teacher_outputs = self.teacher_model(inputs)

        distillation_loss = 0
     
        if self.distillation_type == 'soft':
            T = self.tau
            distillation_loss = F.kl_div(F.log_softmax(outputs_kd / T, dim=1),
                                         F.log_softmax(teacher_outputs / T, dim=1),
                                         reduction='sum', log_target=True) * (T ** 2) / outputs_kd.numel()
        elif self.distillation_type == 'hard':
            distillation_loss = F.cross_entropy(outputs_kd, teacher_outputs.argmax(dim=1))

        loss = base_loss * (1 - self.alpha) + distillation_loss * self.alpha
        return loss