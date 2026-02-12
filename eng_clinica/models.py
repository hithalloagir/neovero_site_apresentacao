from django.db import models


class ConsultaOsNew(models.Model):
    id_hash = models.CharField(primary_key=True, max_length=32)
    empresa = models.CharField(max_length=50, blank=True, null=True)
    razaosocial = models.TextField(blank=True, null=True)
    grupo_setor = models.TextField(blank=True, null=True)
    os = models.CharField(max_length=50, blank=True, null=True)
    oficina = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    prioridade = models.CharField(max_length=50, blank=True, null=True)
    complexidade = models.CharField(max_length=100, blank=True, null=True)
    tag = models.CharField(max_length=100, blank=True, null=True)
    patrimonio = models.CharField(max_length=100, blank=True, null=True)
    sn = models.CharField(max_length=100, blank=True, null=True)
    equipamento = models.TextField(blank=True, null=True)
    setor = models.TextField(blank=True, null=True)
    abertura = models.DateTimeField(blank=True, null=True)
    parada = models.DateTimeField(blank=True, null=True)
    funcionamento = models.DateTimeField(blank=True, null=True)
    fechamento = models.DateTimeField(blank=True, null=True)
    data_atendimento = models.DateTimeField(blank=True, null=True)
    data_solucao = models.DateTimeField(blank=True, null=True)
    data_chamado = models.DateTimeField(blank=True, null=True)
    ocorrencia = models.TextField(blank=True, null=True)
    causa = models.TextField(blank=True, null=True)
    fornecedor = models.TextField(blank=True, null=True)
    custo_os = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    custo_mo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    custo_peca = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    custo_servicoexterno = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    responsavel = models.TextField(blank=True, null=True)
    solicitante = models.TextField(blank=True, null=True)
    os_comentario_tecnico = models.TextField(blank=True, null=True)
    tipomanutencao = models.CharField(max_length=100, blank=True, null=True)
    situacao = models.CharField(max_length=100, blank=True, null=True)
    colaborador_mo = models.TextField(blank=True, null=True)
    data_inicial_mo = models.DateTimeField(blank=True, null=True)
    data_fim_mo = models.DateTimeField(blank=True, null=True)
    qtd_mo_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    obs_mo = models.TextField(blank=True, null=True)
    servico = models.TextField(blank=True, null=True)
    requisicao = models.CharField(max_length=50, blank=True, null=True)
    avaliacao = models.TextField(blank=True, null=True)
    obs_requisicao = models.TextField(blank=True, null=True)
    pendencia = models.TextField(blank=True, null=True)
    inicio_pendencia = models.DateTimeField(blank=True, null=True)
    fechamento_pendencia = models.DateTimeField(blank=True, null=True)
    local_api = models.CharField(max_length=50, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consulta_os_new'


class EtlLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    pipeline_name = models.TextField()
    source_name = models.TextField()
    window_start = models.DateTimeField()
    window_end = models.DateTimeField()
    status = models.TextField()
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(blank=True, null=True)
    records_loaded = models.IntegerField()
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'etl_log'


class EtlWatermark(models.Model):
    pk = models.CompositePrimaryKey('pipeline_name', 'source_name')
    pipeline_name = models.TextField()
    source_name = models.TextField()
    last_success_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'etl_watermark'


class ConsultaEquipamentos(models.Model):
    id_hash = models.CharField(primary_key=True, max_length=32)
    empresa = models.CharField(max_length=255, blank=True, null=True)
    grupo_setor = models.CharField(max_length=255, blank=True, null=True)
    setor = models.CharField(max_length=255, blank=True, null=True)
    familia = models.CharField(max_length=255, blank=True, null=True)
    modelo = models.CharField(max_length=255, blank=True, null=True)
    tipoequipamento = models.CharField(max_length=255, blank=True, null=True)
    fabricante = models.CharField(max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    nserie = models.CharField(max_length=255, blank=True, null=True)
    tombamento = models.CharField(max_length=255, blank=True, null=True)
    cadastro = models.DateTimeField(blank=True, null=True)
    instalacao = models.DateTimeField(blank=True, null=True)
    garantia = models.DateTimeField(blank=True, null=True)
    local_api = models.CharField(max_length=50, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consulta_equipamentos'
